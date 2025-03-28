import tkinter as tk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import re


class SpamPhishingDetector:
    def __init__(self, root):
        self.result_type = None
        self.model = make_pipeline(TfidfVectorizer(stop_words='english'), MultinomialNB())
        self.train_model()
        self.accent_color = "#e44c65"
        self.root = root
        self.root.title("InboxDefender")
        self.root.geometry("650x550")
        self.root.configure(bg="#2e3440")
        root.iconbitmap("logoo.ico")

        self.title_label = tk.Label(
            root, text="Inbox Defender",
            font=("Segoe UI", 22, 'bold'),
            fg=self.accent_color, bg="#2e3440"
        )
        self.title_label.pack(pady=(20, 5))

        self.label = tk.Label(
            root, text="Paste or Type the Email Content Below:",
            font=("Segoe UI", 14),
            fg="#d8dee9", bg="#2e3440"
        )
        self.label.pack(pady=(10, 10))

        self.textbox = tk.Text(
            root, height=12, width=60,
            font=("Consolas", 12),
            bg="#3b4252", fg="#eceff4",
            insertbackground="#eceff4",
            bd=2, relief="flat", padx=10, pady=10
        )
        self.textbox.pack(pady=10)

        self.check_button = tk.Button(
            root, text="Analyze Email",
            command=self.check_spam_phishing,
            font=("Segoe UI", 12, 'bold'),
            bg=self.accent_color, fg="#eceff4",
            activebackground="#d93c58",
            activeforeground="#2e3440",
            relief="flat", bd=0,
            padx=20, pady=10,
            cursor="hand2"
        )
        self.check_button.pack(pady=(15, 10))

        self.result_label = tk.Label(
            root, text="",
            font=("Segoe UI", 14, 'bold'),
            fg="#a3be8c", bg="#2e3440"
        )
        self.result_label.pack(pady=10)

        self.explanation_label = tk.Label(
            root, text="",
            wraplength=450, justify="left",
            font=("Segoe UI", 12),
            fg="#eceff4", bg="#2e3440"
        )
        self.explanation_label.pack(pady=20)
        self.explanation_label.pack_forget()

        self.back_button = tk.Button(
            root, text="Back to Analyze Again",
            command=self.back_to_analyze,
            font=("Segoe UI", 12, 'bold'),
            bg=self.accent_color, fg="#eceff4",
            activebackground="#d93c58",
            activeforeground="#2e3440",
            relief="flat", bd=0,
            padx=20, pady=15,
            cursor="hand2"
        )
        self.back_button.pack(pady=(30, 10))
        self.back_button.pack_forget()

    def on_hover_enter(self, event):
        self.check_button.config(bg="#d93c58")

    def on_hover_leave(self, event):
        self.check_button.config(bg=self.accent_color)

    def train_model(self):
        data = [
            ("ham", "Go until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat..."),
            ("ham", "Ok lar... Joking wif u oni..."),
            ("spam", "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"),
            ("ham", "U dun say so early hor... U c already then say..."),
            ("ham", "Nah I don't think he goes to usf, he lives around here though"),
            ("spam", "FreeMsg Hey there darling it's been 3 week's now and no word back! I'd like some fun you up for it still? Tb ok! XxX std chgs to send, £1.50 to rcv"),
            ("ham", "Even my brother is not like to speak with me. They treat me like aids patent."),
            ("ham", "As per your request 'Melle Melle (Oru Minnaminunginte Nurungu Vettam)' has been set as your callertune for all Callers. Press *9 to copy your friends Callertune"),
            ("spam", "WINNER!! As a valued network customer you have been selected to receive a £900 prize reward! To claim call 09061701461. Claim code KL341. Valid 12 hours only."),
            ("spam", "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free! Call The Mobile Update Co FREE on 08002986030"),
            ("ham", "I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k? I've cried enough today."),
            ("spam", "SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575. Cost 150p/day, 6days, 16+ TsandCs apply Reply HL 4 info"),
            ("spam", "URGENT! You have won a 1 week FREE membership in our £100,000 Prize Jackpot! Txt the word: CLAIM to No: 81010 T&C www.dbuk.net LCCLTD POBOX 4403LDNW1A7RW18"),
            ("ham", "I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times."),
            ("ham", "I HAVE A DATE ON SUNDAY WITH WILL!!"),
            ("spam", "XXXMobileMovieClub: To use your credit, click the WAP link in the next txt message or click here>> http://wap.xxxmobilemovieclub.com?n=QJKGIGHJJGCBL"),
            ("ham", "Oh k...i'm watching here:)"),
            ("ham", "Nah, I don't think he goes to usf, he lives around here though."),
            ("ham", "Fine if that's the way u feel. That's the way its gota b"),
            ("spam", "England v Macedonia - dont miss the goals/team news. Txt ur national team to 87077 eg ENGLAND to 87077 Try:WALES, SCOTLAND 4txt/ú1.20 POBOXox36504W45WQ 16+"),
            ("ham", "Is that seriously how you spell his name?"),
            ("ham", "I‘m going to try for 2 months ha ha only joking"),
            ("ham", "So ü pay first lar... Then when is da stock comin..."),
            ("ham", "Aft i finish my lunch then i go str down lor. Ard 3 smth lor. U finish ur lunch already?"),
            ("ham", "Ffffffffff. Alright no way I can meet up with you sooner?"),
            ("ham", "Just forced myself to eat a slice. I'm really not hungry tho. This sucks. Mark is getting worried. He knows I'm sick when I turn down pizza. Lol"),
            ("ham", "Lol your always so convincing."),
            ("ham", "Did you catch the bus ? Are you frying an egg ? Did you make a tea? Are you eating your mom's left over dinner ? Do you feel my Love ?"),
            ("ham", "I'm back & we're packing the car now, I'll let you know if there's room"),
            ("ham", "Ahhh. Work. I vaguely remember that! What does it feel like? Lol"),
            ("ham", "Wait that's still not all that clear, were you not sure about me being sarcastic or that that's why x doesn't want to live")
        ]
        labels = [1 if label == 'spam' else 0 for label, _ in data]
        messages = [message for _, message in data]
        self.model.fit(messages, labels)

    def detect_phishing(self, text):
        patterns = [
            r"payp[a@]l",
            r"amaz[o0]n",
            r"free[\s]*gift[\s]*card",
            r"verify[\s]*account",
            r"urgent",
            r"claim[\s]*your[\s]*prize",
            r"limited[\s]*time[\s]*offer",
            r"free[\s]*vacation[\s]*package",
            r"congratulations[\s]*you[\s]*won",
        ]
        for pattern in patterns:
            if re.search(pattern, text.lower()):
                return True
        return False

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        return text.strip()

    def check_spam_phishing(self):
        email_body = self.textbox.get("1.0", "end-1c")
        cleaned_text = self.clean_text(email_body)

        if self.detect_phishing(email_body):
            self.result_type = "phishing"
            self.result_label.config(text="⚠️ Phishing Message / Email Detected!", fg="#bf616a")
            text = (
                "⚠️ This Message / Email was flagged as Phishing because it contained some of the following suspicious elements:\n"
                "- 'Verify account'\n"
                "- 'Claim your prize'\n"
                "- 'Free vacation package'\n"
                "- Brand impersonation (Amazon, PayPal, etc.)\n\n"

            )
            color = "#bf616a"
        elif self.model.predict([cleaned_text])[0] == 1:
            self.result_type = "spam"
            self.result_label.config(text="🚫 Spam Message / Email Detected!", fg="#d08770")
            text = (
                "🚫 This Message / Email was flagged as Spam based on its content.\n"
                "It likely contains promotional, repetitive, or misleading information.\n\n"

            )

        else:
            self.result_type = "ham"
            self.result_label.config(text="✅ This Message / Email Is Safe", fg="#a3be8c")
            text = (
                "✅  This Message / Email contained no suspicious patterns or spam behavior were detected. "
                "It seems safe to open any links."
            )
            color = "#a3be8c"

        self.explanation_label.config(text=text, fg="white")
        self.explanation_label.pack(pady=20)

        self.back_button.pack(pady=(30, 10))

        self.textbox.pack_forget()
        self.check_button.pack_forget()

    def back_to_analyze(self):
        self.explanation_label.pack_forget()
        self.back_button.pack_forget()
        self.result_label.config(text="")

        self.textbox.pack(pady=10)
        self.check_button.pack(pady=(15, 10))


if __name__ == "__main__":
    root = tk.Tk()
    app = SpamPhishingDetector(root)
    root.mainloop()
