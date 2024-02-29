import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import dns.resolver

def enumerate_subdomains(domain):
    subdomains = ['www','mail','ftp','localhost','webmail','smtp','pop','ns1','webdisk','ns2','cpanel','whm','autodiscover','autoconfig','m','imap','test','ns','blog','pop3','dev','www2','admin','forum','news','vpn','ns3','mail2','new','mysql','old','lists','support','mobile','mx','static','docs','beta','shop','sql','secure','demo','cp','calendar','wiki','web','media','email','images','img','www1','intranet','portal','video','sip','dns2','api','cdn','stats','dns1','ns4','www3','dns','search','staging','server','mx1','chat','wap','my','svn','mail1','sites','proxy','ads','host','crm','cms','backup','mx2','lyncdiscover','info','apps','download','remote','db','forums','store','relay','files','newsletter','app','live','owa','en','start','sms','office','exchange','ipv4']
    valid_subdomains = []
    for subdomain in subdomains:
        try:
            answers = dns.resolver.resolve(f'{subdomain}.{domain}', 'A')
            for _ in answers:
                valid_subdomains.append(f'{subdomain}.{domain}')
        except Exception:
            pass
    return valid_subdomains


def dns_enumeration(domain):
    record_types = ['A', 'AAAA', 'NS', 'CNAME', 'MX', 'PTR', 'SOA', 'TXT']
    records_result = {}
    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            records_result[record] = [answer.to_text() for answer in answers]
        except Exception:
            records_result[record] = ['No record found']
    return records_result

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DNS & Subdomain Enumeration Tool")
        self.geometry("800x600")  # Larger size
        self.configure(background='light gray')

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)

        self.option = tk.StringVar()
        self.option.set("")  # Set an empty string initially

        subdomain_button = tk.Radiobutton(self, text="Subdomain Enumeration", variable=self.option, value="subdomain_enum", bg='gray', selectcolor='green', font=('Arial', 12))
        subdomain_button.pack(pady=10)

        dns_button = tk.Radiobutton(self, text="DNS Enumeration", variable=self.option, value="dns_enum", bg='gray', selectcolor='green', font=('Arial', 12))
        dns_button.pack(pady=10)

        tk.Label(self, text="Enter Domain (e.g., example.com):", bg='light gray').pack()

        self.domain_entry = tk.Entry(self, font=('Arial', 12))
        self.domain_entry.pack()

        execute_button = tk.Button(self, text="Execute", command=self.execute, bg='blue', fg='white', font=('Arial', 12))
        execute_button.pack(pady=10)

        save_button = tk.Button(self, text="Save Results", command=self.save_results, bg='orange', fg='black', font=('Arial', 12))
        save_button.pack(pady=10)

        self.result_frame = tk.Frame(self, bg='light green')
        self.result_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output = tk.Text(self.result_frame, height=12, bg='light green', font=('Arial', 12))
        self.output.pack(fill=tk.BOTH, expand=True)

    def execute(self):
        domain = self.domain_entry.get().replace("https://", "").replace("http://", "")
        if not domain:
            messagebox.showerror("Error", "Please enter a main domain.")
            return
        if self.option.get() == "subdomain_enum":
            result = enumerate_subdomains(domain)
            message = "\n".join(result)
        else:
            records = dns_enumeration(domain)
            message = "\n".join([f"{record}: {', '.join(values)}" for record, values in records.items()])
        self.display_output(message)

    def display_output(self, message):
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, message)
        self.output.config(state='disabled')

    def save_results(self):
        response = messagebox.askyesno("Save Results", "Do you want to save the results?")
        if response:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.output.get("1.0", tk.END))
                messagebox.showinfo("Save Results", f"Results saved to {file_path}")

    def show_about(self):
        messagebox.showinfo("About", "This tool allows for DNS and subdomain enumeration.")

    def show_help(self):
        messagebox.showinfo("Help", "This section provides guidance on how to use the tool effectively. Choose 'Subdomain Enumeration' to find active subdomains for a given domain. Select 'DNS Enumeration' to query different DNS record types for a domain. Enter the domain name without protocols (e.g., 'example.com') in the provided field, then click 'Execute' to see the results. Use 'Save Results' to save the output.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
