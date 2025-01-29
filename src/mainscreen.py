import customtkinter as ctk
import pygame
import os
import threading
import webbrowser
import asyncio  # 追加

# Set the appearance mode and default color theme to light
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")  # "light" から "green" に変更

class SoundStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SoundStudio β1.0")
        self.geometry("900x600")
        self.configure(bg="#F2F2F2")
        self.attributes("-fullscreen", True)

        self.music_files = {}
        self.current_song = None
        self.current_category = None
        self.is_playing = False

        self.create_widgets()
        self.load_music_files()

        pygame.mixer.init()  # pygame.mixerの初期化
        self.loop = asyncio.get_event_loop()  # イベントループの作成

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(
            self, text="SoundStudio β1.0", font=("Helvetica", 32, "bold"), fg_color="#D8E0BB", text_color="#333333"
        )
        self.title_label.pack(fill="x", pady=(20, 10))

        main_frame = ctk.CTkFrame(self, fg_color="#E6E6E6", corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.tab_view = ctk.CTkTabview(main_frame)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        control_frame = ctk.CTkFrame(main_frame, fg_color="#D1E9A8", corner_radius=10)
        control_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.song_label = ctk.CTkLabel(
            control_frame, text="曲が選択されていません", font=("Helvetica", 20), fg_color="#C1D7A4", text_color="#333333"
        )
        self.song_label.pack(pady=(30, 15))

        buttons_frame = ctk.CTkFrame(control_frame, fg_color="#D1E9A8")
        buttons_frame.pack(pady=20)

        play_button = ctk.CTkButton(buttons_frame, text="▶", font=("Helvetica", 24, "bold"), command=self.play_song, width=80, height=80)
        play_button.grid(row=0, column=1, padx=20)

        pause_button = ctk.CTkButton(buttons_frame, text="⏸", font=("Helvetica", 24, "bold"), command=self.pause_song, width=80, height=80)
        pause_button.grid(row=0, column=2, padx=20)

        stop_button = ctk.CTkButton(buttons_frame, text="⏹", font=("Helvetica", 24, "bold"), command=self.stop_song, width=80, height=80)
        stop_button.grid(row=0, column=3, padx=20)

        close_button = ctk.CTkButton(control_frame, text="終了", font=("Helvetica", 18), command=self.exit_app, fg_color="#FF6B6B", width=120, height=50)
        close_button.pack(pady=10)

        self.volume_slider = ctk.CTkSlider(control_frame, from_=0, to=1, command=self.set_volume, width=250)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(control_frame, width=300, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # ウェブサイトへ飛ぶボタンを右下に配置
        website_button = ctk.CTkButton(control_frame, text="ウェブサイトへ", font=("Helvetica", 12), command=self.open_website, fg_color="#B9DABA", width=100, height=30)
        website_button.pack(side="bottom", anchor="se", padx=10, pady=10)  # 右下に配置

        # ログウィジェットの作成
        self.log_text = ctk.CTkTextbox(self, width=800, height=150)
        self.log_text.pack(pady=10, padx=20, fill="x")

        # 設定タブの作成
        self.settings_tab = ctk.CTkTabview(main_frame)
        self.settings_tab.add("設定")

        self.create_settings_tab()

        # ライセンスと開発者情報
        footer_frame = ctk.CTkFrame(self, fg_color="#F2F2F2")
        footer_frame.pack(side="bottom", fill="x", pady=10)

        license_label = ctk.CTkLabel(footer_frame, text="Apache 2.0 License", font=("Helvetica", 10), text_color="#333333")
        license_label.pack(side="left", padx=20)

        developer_label = ctk.CTkLabel(footer_frame, text="Developed by TechFish", font=("Helvetica", 10), text_color="#333333")
        developer_label.pack(side="right", padx=20)

    def open_website(self):
        # ウェブサイトを開くための関数
        webbrowser.open("https://sound-studio-dev.vercel.app/")

    def create_settings_tab(self):
        settings_frame = ctk.CTkFrame(self.settings_tab)  # ここはそのまま
        settings_frame.grid(padx=20, pady=20, sticky="nsew")  # pack() を grid() に変更

        # ボタンの色変更
        color_label = ctk.CTkLabel(settings_frame, text="ボタンの色を選択", font=("Helvetica", 16))
        color_label.grid(row=0, column=0, pady=(0, 10))

        self.button_color_entry = ctk.CTkEntry(settings_frame, placeholder_text="例: #FF0000")
        self.button_color_entry.grid(row=1, column=0, pady=(0, 10))

        apply_color_button = ctk.CTkButton(settings_frame, text="色を適用", command=self.apply_button_color)
        apply_color_button.grid(row=2, column=0, pady=(10, 10))

        # フォントサイズ調整
        font_size_label = ctk.CTkLabel(settings_frame, text="フォントサイズを調整", font=("Helvetica", 16))
        font_size_label.grid(row=3, column=0, pady=(20, 10))

        self.font_size_slider = ctk.CTkSlider(settings_frame, from_=12, to=32, command=self.change_font_size)
        self.font_size_slider.set(20)  # 初期値
        self.font_size_slider.grid(row=4, column=0, pady=(0, 10))

        # 変更を適用するボタン
        apply_button = ctk.CTkButton(settings_frame, text="適用", command=self.apply_settings)
        apply_button.grid(row=5, column=0, pady=(10, 20))


    def change_font_size(self, size):
        # フォントサイズを変更
        new_size = int(size)
        self.title_label.configure(font=("Helvetica", new_size, "bold"))
        self.song_label.configure(font=("Helvetica", new_size))
        for widget in self.tab_view.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(font=("Helvetica", new_size))

    def apply_settings(self):
        # 設定の適用
        color = self.button_color_entry.get()
        self.apply_button_color()
        self.change_font_size(self.font_size_slider.get())

    def apply_button_color(self):
        # ボタンの色を適用
        color = self.button_color_entry.get()
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(bg=color)

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def load_music_files(self):
        music_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'musics')
        self.log("音楽ファイルを読み込み中...")
        try:
            if os.path.exists(music_dir) and os.path.isdir(music_dir):
                for root, dirs, files in os.walk(music_dir):
                    for file in files:
                        if file.endswith('.mp3'):
                            category = os.path.basename(root)
                            if category not in self.music_files:
                                self.music_files[category] = []
                            self.music_files[category].append(file)
                            self.create_bgm_tab(category, self.music_files[category])
                self.log("音楽ファイルの読み込みが完了しました。")
            else:
                self.log("musicsフォルダが存在しないか、ディレクトリではありません。")
        except Exception as e:
            self.log(f"音楽ファイルの読み込み中にエラーが発生しました: {str(e)}")

    def create_bgm_tab(self, category, files):
        tab = self.tab_view.add(category)
        for index, file in enumerate(files):
            button = ctk.CTkButton(
                tab, text=file, command=lambda f=file, c=category: self.play_selected_song(f, c),
                font=("Helvetica", 18), width=180, height=50, fg_color="#B9DABA", text_color="#333333", corner_radius=8
            )
            button.grid(row=index, column=0, sticky="ew", padx=15, pady=8)


    def play_selected_song(self, song: str, category: str) -> None:
        song_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'musics', category, song)
        self.current_song = song
        self.current_category = category
        try:
            if not os.path.exists(song_path):
                self.log(f"ファイルが存在しません: {song_path}")
                return
            
            threading.Thread(target=self._play_song, args=(song_path,)).start()
            self.log(f"{song}を{category}から再生します。")
        except Exception as e:
            self.log(f"'{song}'の再生中にエラーが発生しました: {str(e)}")

    def _play_song(self, song_path):
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.loop.create_task(self.update_progress_bar())  # 非同期タスクの作成
        except Exception as e:
            self.log(f"曲の再生中にエラーが発生しました: {str(e)}")

    def play_song(self):
        if self.current_song:
            threading.Thread(target=self._resume_song).start()
            self.log(f"{self.current_song}の再生を再開します。")

    def _resume_song(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.update_progress_bar()

    def pause_song(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.log(f"{self.current_song}の再生を一時停止します。")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.progress_bar.set(0)
        self.song_label.configure(text="曲が選択されていません")
        self.current_song = None
        self.current_category = None
        self.log("曲の再生を停止します。")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))
        self.log(f"音量を{volume}に設定します。")

    async def update_progress_bar(self):
        while self.is_playing and self.current_song:
            current_time = pygame.mixer.music.get_pos() / 1000
            try:
                song_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'musics', self.current_category, self.current_song)
                total_length = pygame.mixer.Sound(song_path).get_length()
                
                progress = current_time / total_length
                self.progress_bar.set(progress)
                await asyncio.sleep(0.5)  # 0.5秒待機
            except Exception as e:
                self.log(f"進度バーの更新中にエラーが発生しました: {str(e)}")
                break

    def exit_app(self):
        self.log("アプリを終了します。")
        pygame.mixer.music.stop()
        self.destroy()