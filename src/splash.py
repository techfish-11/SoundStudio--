import customtkinter as ctk
import time

class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SoundStudio β1.0")
        self.geometry("900x600")
        self.configure(bg="#F2F2F2")
        self.attributes("-fullscreen", True)

        # スプラッシュ画面のUIの作成
        self.create_splash_widgets()

        # スプラッシュ画面を3秒間表示
        self.after(3000, self.destroy)
        
    def create_splash_widgets(self):
        splash_label = ctk.CTkLabel(
            self, text="SoundStudio β1.0", font=("Helvetica", 56, "bold"), fg_color="#D8E0BB", text_color="#333333"
        )
        splash_label.pack(fill="x", pady=(80, 20))

        usage_label = ctk.CTkLabel(
            self, text="使用方法:\n1. 音楽カテゴリから曲を選択\n2. 再生ボタンをクリックして再生\n3. 一時停止ボタンで一時停止\n4. 停止ボタンで停止\n5. 音量スライダーで音量調整", font=("Helvetica", 24), fg_color="#F2F2F2", text_color="#333333"
        )
        usage_label.pack(fill="x", pady=(10, 5))

        developed_by_label = ctk.CTkLabel(
            self, text="Developed by TechFish", font=("Helvetica", 28), fg_color="#F2F2F2", text_color="#333333"
        )
        developed_by_label.pack(fill="x", pady=(10, 5))

        license_label = ctk.CTkLabel(
            self, text="Apache 2.0 License", font=("Helvetica", 24), fg_color="#F2F2F2", text_color="#333333"
        )
        license_label.pack(fill="x", pady=(5, 50))

        self.fade_in()

    def fade_in(self):
        for i in range(11):
            self.attributes("-alpha", i * 0.1)  # 透明度を設定
            self.update()
            time.sleep(0.1)  # 小さな待機時間