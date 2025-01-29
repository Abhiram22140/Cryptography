import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import random
import time
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io

# Function to generate random bitstrings
def random_bitstring(length):
    return np.random.choice(['0', '1'], size=length)

# BB84 Protocol with Visualization, Error Checking, and Eavesdropping Simulation
def bb84_protocol_visualized(length=8, error_rate=0.1, eavesdropping=False, update_step=None, max_error_rate=0.25):
    alice_bits = random_bitstring(length)
    alice_bases = random_bitstring(length)
    bob_bases = random_bitstring(length)
    key = []
    simulator = AerSimulator()
    errors = 0
    error_rates = []  # Track error rates for each step
    entropy_values = []  # Track entropy at each step

    for i in range(length):
        qc = QuantumCircuit(1, 1)
        if alice_bases[i] == '0':  # Z-basis
            if alice_bits[i] == '1':
                qc.x(0)
        else:  # X-basis
            qc.h(0) if alice_bits[i] == '0' else qc.x(0); qc.h(0)

        if bob_bases[i] == '1':
            qc.h(0)
        qc.measure(0, 0)

        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit).result()
        measured_bit = list(result.get_counts().keys())[0]

        # Introduce noise due to the error rate
        if random.random() < error_rate:
            measured_bit = '1' if measured_bit == '0' else '0'

        # Simulate Eavesdropping (Eve introduces additional errors)
        if eavesdropping:
            if random.random() < error_rate:
                measured_bit = '1' if measured_bit == '0' else '0'

        if alice_bases[i] == bob_bases[i]:
            key.append(measured_bit)
            if measured_bit != alice_bits[i]:
                errors += 1

        # Track error rate and entropy
        error_rate_step = errors / (i + 1)
        entropy_values.append(calculate_entropy(''.join(key)))
        error_rates.append(error_rate_step)

        # Visualization step
        if update_step:
            update_step(i, alice_bits, alice_bases, bob_bases, measured_bit)

        # Check if the error rate exceeds the threshold
        if error_rate_step > max_error_rate:
            # Key rejection occurs if the error rate is too high
            return "Key Rejected: High Error Rate", error_rates, entropy_values

    qber = errors / length if length > 0 else 0
    return ''.join(key), qber, error_rates, entropy_values

# AES Encryption using QKD Key
def aes_encrypt(data, key):
    cipher = AES.new(key.encode('utf-8')[:16], AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def aes_decrypt(encrypted_data, key):
    raw_data = base64.b64decode(encrypted_data)
    iv = raw_data[:AES.block_size]
    cipher = AES.new(key.encode('utf-8')[:16], AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(raw_data[AES.block_size:]), AES.block_size)
    return plaintext

# Key Padding
def pad_key(key, required_length=16):
    while len(key) < required_length:
        key += key[:required_length - len(key)]
    return key[:required_length]

# Calculate Entropy (Key Strength)
def calculate_entropy(key):
    counts = np.array([key.count('0'), key.count('1')])
    return entropy(counts, base=2)

# GUI Application
class QuantumCryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Cryptography with BB84 and AES")
        self.root.geometry("1000x700")

        # Title Label
        ttk.Label(root, text="Quantum Cryptography Simulation", font=("Arial", 16)).pack(pady=10)

        # Key Length Input
        self.key_length_var = tk.IntVar(value=32)
        ttk.Label(root, text="Key Length (bits):").pack(pady=5)
        self.key_length_spinbox = ttk.Spinbox(root, from_=8, to=128, increment=8, textvariable=self.key_length_var)
        self.key_length_spinbox.pack(pady=5)

        # Error Rate Input
        self.error_rate_var = tk.DoubleVar(value=0.1)
        ttk.Label(root, text="Error Rate:").pack(pady=5)
        self.error_rate_spinbox = ttk.Spinbox(root, from_=0, to=0.5, increment=0.01, textvariable=self.error_rate_var)
        self.error_rate_spinbox.pack(pady=5)

        # Eavesdropping Option
        self.eavesdropping_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, text="Simulate Eavesdropping", variable=self.eavesdropping_var).pack(pady=5)

        # Data Input
        ttk.Label(root, text="Enter Data to Encrypt:").pack(pady=5)
        self.data_entry = tk.Entry(root, width=50)
        self.data_entry.insert(0, "Smart Grid Status: Operational")  # Default data
        self.data_entry.pack(pady=5)

        # Image Selection
        ttk.Button(root, text="Select Image to Encrypt", command=self.select_image).pack(pady=10)

        # Image Display
        self.image_label = ttk.Label(root, text="Selected Image will appear here")
        self.image_label.pack(pady=5)

        # Visualization Area
        ttk.Label(root, text="BB84 Protocol Visualization:").pack(pady=5)
        self.visualization_text = tk.Text(root, height=5, wrap=tk.WORD)
        self.visualization_text.pack(pady=5)

        # Buttons
        ttk.Button(root, text="Run BB84 Protocol", command=self.run_bb84).pack(pady=10)
        ttk.Button(root, text="Encrypt & Decrypt Data", command=self.encrypt_decrypt).pack(pady=10)
        ttk.Button(root, text="Encrypt & Decrypt Image", command=self.encrypt_decrypt_image).pack(pady=10)

        # Output Text
        self.output_text = tk.Text(root, height=5, wrap=tk.WORD)
        self.output_text.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.gif")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((100, 100))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk, text="")
            self.image_label.image = img_tk

    def update_visualization(self, step, alice_bits, alice_bases, bob_bases, measured_bit):
        self.visualization_text.insert(
            tk.END,
            f"Step {step+1}:\n"
            f"Alice Bit: {alice_bits[step]}, Alice Basis: {alice_bases[step]}\n"
            f"Bob Basis: {bob_bases[step]}, Measured Bit: {measured_bit}\n\n"
        )
        self.visualization_text.see(tk.END)
        self.root.update()

    def run_bb84(self):
        key, qber, error_rates, entropy_values = bb84_protocol_visualized(
            length=self.key_length_var.get(),
            error_rate=self.error_rate_var.get(),
            eavesdropping=self.eavesdropping_var.get(),
            update_step=self.update_visualization,
        )
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Key: {key}\nQBER: {qber}\n")
        self.show_graph_window(error_rates, entropy_values)

    def encrypt_decrypt(self):
        data = self.data_entry.get()
        key = ''.join(random_bitstring(self.key_length_var.get()))  # QKD-generated key
        encrypted_data = aes_encrypt(data.encode('utf-8'), key)
        decrypted_data = aes_decrypt(encrypted_data, key)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Original Data: {data}\nEncrypted Data: {encrypted_data}\nDecrypted Data: {decrypted_data.decode('utf-8')}\n")

    def encrypt_decrypt_image(self):
        if hasattr(self, 'image_path'):
            with open(self.image_path, 'rb') as image_file:
                image_data = image_file.read()

            key = ''.join(random_bitstring(self.key_length_var.get()))  # QKD-generated key
            encrypted_image = aes_encrypt(image_data, key)
            decrypted_image_data = aes_decrypt(encrypted_image, key)

            decrypted_image = Image.open(io.BytesIO(decrypted_image_data))
            decrypted_image.show()

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Image Encrypted and Decrypted Successfully")
        else:
            messagebox.showerror("Error", "Please select an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumCryptoApp(root)
    root.mainloop()
