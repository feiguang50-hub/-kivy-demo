import tkinter as tk
from tkinter import messagebox, ttk
import random, os
class PM_LeanSandtable:
    def __init__(self, root):
        self.root = root
        self.root.title("谁是卧底 —— 工管数字沙盘精简版")
        self.root.geometry("880x680")
        self.root.configure(bg="#F1F5F9")
        # 核心配色
        self.C_PRIMARY = "#1E3A8A"; self.C_ALERT = "#DC2626"; self.C_SUCCESS = "#16A34A"; self.C_GOLD = "#D97706"
        self.word_bank = [
            ("横道图", "网络图"), ("关键线路", "非关键线路"), ("总时差", "自由时差"), ("赶工", "资源优化"),
            ("工程变更", "工程索赔"), ("不可抗力", "合同风险"), ("固定总价合同", "单价合同"), ("BIM技术", "数字孪生")
        ]
        self.punishments = [
            "现场用肢体语言模仿'挖掘机施工'或'吊车起吊' 🏗️",
            "用'痛失一标段'的悲伤语气，朗读工管教材上的任意一句话 😭",
            "现场科普：为什么混凝土浇筑不能断？说得好免罚 💡",
            "假设你是项目经理，对全班进行30秒的'安全早会训话' 🤬"
        ]
        self.rewards = [
            "🏆【国家鲁班奖】：本周工程实训作业，获得一次'免签批改'（普通错漏不扣分）！",
            "💰【顺利结算奖】：期末总评成绩争取'监理友情赞助 1 分'（或出局队友请喝饮料）！",
            "☕【甲方爸爸的咖啡】：获得由现场'带班总监（老师）'请喝下午茶的机会！"
        ]
        self.skill_cards = [
            "🚨【基坑坍塌】：深基坑出现位移！指定选手本轮发言严禁说'成本、进度、质量'！",
            "🌧️【不可抗力】：遭遇特大暴雨现场停工！分包索赔。这一轮发言顺序倒序进行！",
            "📜【设计变更】：图纸紧急变更！所有人本轮发言倒计时强制压缩至10秒！",
            "💸【劳务纠纷】：分包商涉嫌挪用劳务费导致工人堵门！被指定选手下一轮不能投票！"
        ]
        self.evm_cv = 15.0; self.evm_sv = -10.0; self.timer_seconds = 30; self.timer_running = False
        self.setup_start_screen()
    def create_btn(self, parent, text, bg, cmd, f_size=11):
        return tk.Button(parent, text=text, font=("Microsoft YaHei", f_size, "bold"), bg=bg, fg="white", bd=0, cursor="hand2", padx=15, pady=5, command=cmd)
    def setup_start_screen(self):
        for w in self.root.winfo_children(): w.destroy()
        self.timer_running = False
        tk.Label(self.root, text="🏛️ 谁是卧底 · 工管智慧沙盘 (精简版)", font=("Microsoft YaHei", 20, "bold"), fg=self.C_PRIMARY, bg="#F1F5F9").pack(pady=30)
        card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        card.pack(padx=80, pady=10, fill="both", expand=True)
        gf = tk.Frame(card, bg="white")
        gf.pack(expand=True, pady=20)
        tk.Label(gf, text="总人数:", font=("Microsoft YaHei", 12), bg="white").grid(row=0, column=0, pady=15, sticky="e")
        self.spin_t = ttk.Spinbox(gf, from_=3, to=20, width=5, font=("Helvetica", 12)); self.spin_t.set(6); self.spin_t.grid(row=0, column=1, padx=10)
        tk.Label(gf, text="卧底数:", font=("Microsoft YaHei", 12), bg="white").grid(row=1, column=0, pady=15, sticky="e")
        self.spin_u = ttk.Spinbox(gf, from_=1, to=5, width=5, font=("Helvetica", 12)); self.spin_u.set(1); self.spin_u.grid(row=1, column=1, padx=10)
        tk.Label(gf, text="自定义A/B (可选):", font=("Microsoft YaHei", 12), bg="white").grid(row=0, column=2, padx=(30,0))
        self.ent_a = tk.Entry(gf, width=12, font=("Microsoft YaHei", 11)); self.ent_a.grid(row=0, column=3)
        self.ent_b = tk.Entry(gf, width=12, font=("Microsoft YaHei", 11)); self.ent_b.grid(row=1, column=3, padx=10)
        self.create_btn(self.root, "🚧 组建项目联合体 🚧", self.C_PRIMARY, self.start_game_logic, 13).pack(pady=40)
    def start_game_logic(self):
        t, u = int(self.spin_t.get()), int(self.spin_u.get())
        if t < 3 or u < 1 or u >= t / 2: return
        w_a, w_b = self.ent_a.get().strip(), self.ent_b.get().strip()
        c_w, u_w = (w_a, w_b) if w_a and w_b else random.choice(self.word_bank)
        if random.choice([True, False]): c_w, u_w = u_w, c_w
        roles = ['平民'] * (t - u) + ['卧底'] * u
        random.shuffle(roles)
        self.players = [{'id': i+1, 'role': roles[i], 'word': u_w if roles[i]=='卧底' else c_w, 'is_alive': True} for i in range(t)]
        self.alive_u, self.alive_c = u, t - u
        self.show_main_screen()
    def show_main_screen(self):
        for w in self.root.winfo_children(): w.destroy()
        # 1. EVM挣值大屏
        db = tk.Frame(self.root, bg="#0F172A", pady=10)
        db.pack(fill="x", padx=30, pady=10)
        self.lbl_evm = tk.Label(db, text=f"📊 动态挣值分析大屏  |  CV (成本偏差): {self.evm_cv:+.1f}万  |  SV (进度偏差): {self.evm_sv:+.1f}万", font=("Microsoft YaHei", 11, "bold"), fg="#34D399", bg="#0F172A")
        self.lbl_evm.pack()
        # 2. 事故指令与倒计时
        ctrl = tk.Frame(self.root, bg="#F1F5F9")
        ctrl.pack(fill="x", padx=30, pady=5)
        acc_card = tk.Frame(ctrl, bg="#FFF1F2", bd=1, relief="solid", padx=10, pady=8)
        acc_card.pack(side="left", fill="x", expand=True)
        self.lbl_sk = tk.Label(acc_card, text="⚠️ 调度指令：请点击右侧下达【突发事故指令】", font=("Microsoft YaHei", 10, "bold"), fg=self.C_ALERT, bg="#FFF1F2", wraplength=450, justify="left")
        self.lbl_sk.pack(side="left")
        def trigger_accident():
            evt = random.choice(self.skill_cards)
            self.lbl_sk.configure(text=evt)
            self.evm_cv -= random.uniform(10, 20); self.evm_sv -= random.uniform(10, 20)
            self.lbl_evm.configure(text=f"📊 动态挣值分析大屏  |  CV: {self.evm_cv:+.1f}万  |  SV: {self.evm_sv:+.1f}万", fg=self.C_ALERT if (self.evm_cv<0 or self.evm_sv<0) else self.C_SUCCESS)
        self.create_btn(acc_card, "⚡ 投产事故", self.C_ALERT, trigger_accident, 9).pack(side="right")
        # ⏱️ 简易计时器
        tm_card = tk.Frame(ctrl, bg="#1E293B", padx=10, pady=8)
        tm_card.pack(side="right", padx=(10, 0))
        self.lbl_tm = tk.Label(tm_card, text="⏱️ 剩余: 30s", font=("Helvetica", 11, "bold"), fg="#F59E0B", bg="#1E293B")
        self.lbl_tm.pack(side="left")
        def toggle_tm():
            if self.timer_running: self.timer_running = False
            else: self.timer_running = True; self.countdown()
        self.create_btn(tm_card, "⏱️ 开/停", self.C_SUCCESS, toggle_tm, 9).pack(side="right", padx=5)
        # 3. 发言流水麦序
        flow = tk.Frame(self.root, bg="white", bd=1, relief="solid", pady=10)
        flow.pack(fill="x", padx=30, pady=10)
        tk.Label(flow, text="🧱 现场工艺施工步序 (在场序列):", font=("Microsoft YaHei", 10, "bold"), fg="#64748B", bg="white").pack(anchor="w", padx=10)
        box = tk.Frame(flow, bg="white")
        box.pack(fill="x", pady=5)
        for p in self.players:
            if p['is_alive']:
                tk.Label(box, text=f" 【{p['id']}号】 \n 正常施工 ", font=("Microsoft YaHei", 9, "bold"), bg="#EFF6FF", fg=self.C_PRIMARY, bd=1, relief="solid", padx=5, pady=2).pack(side="left", padx=5)
        # 4. 终止合同投票
        vote = tk.Frame(self.root, bg="white", bd=1, relief="solid", padx=20, pady=15)
        vote.pack(fill="x", padx=30, pady=5)
        tk.Label(vote, text="🗳️ 决议终止哪个标段的合同？", font=("Microsoft YaHei", 11, "bold"), bg="white").pack(side="left")
        self.cb_vote = ttk.Combobox(vote, values=[p['id'] for p in self.players if p['is_alive']], state="readonly", font=("Helvetica", 12), width=5)
        self.cb_vote.pack(side="left", padx=15)
        self.create_btn(vote, "💥 强制终止合同并审计", self.C_ALERT, self.eliminate_player).pack(side="right")
    def countdown(self):
        if self.timer_running and self.timer_seconds > 0:
            self.timer_seconds -= 1; self.lbl_tm.configure(text=f"⏱️ 剩余: {self.timer_seconds}s")
            self.root.after(1000, self.countdown)
        elif self.timer_seconds == 0:
            self.timer_running = False; messagebox.showwarning("超时", "发言超时，强制中断！"); self.timer_seconds = 30
    def eliminate_player(self):
        sel = self.cb_vote.get()
        if not sel: return
        p = next(x for x in self.players if x['id'] == int(sel))
        p['is_alive'] = False
        messagebox.showinfo("审计底牌", f"💥 审计公示：{p['id']}号 真实身份是 【{p['role']}】！\n底牌词语是：【{p['word']}】")
        messagebox.showwarning("红线处罚", f"🚨 强执现场安全教育惩罚：\n\n{random.choice(self.punishments)}")
        if p['role'] == '卧底': self.alive_u -= 1
        else: self.alive_c -= 1
        if self.alive_u == 0: self.end_game("🎉 正规总包大获全胜！", "恶意挂靠分包已被全部清退。")
        elif self.alive_u >= self.alive_c: self.end_game("😈 违法分包商渗透逆袭！", "卧底成功套现全部工程款。")
        else: self.timer_seconds = 30; self.show_main_screen()
    def end_game(self, title, msg):
        for w in self.root.winfo_children(): w.destroy()
        tk.Label(self.root, text=title, font=("Microsoft YaHei", 20, "bold"), fg=self.C_PRIMARY, bg="#F1F5F9").pack(pady=20)
        rw = tk.Frame(self.root, bg="#FFFBEB", bd=1, relief="solid", padx=25, pady=15)
        rw.pack(fill="x", padx=50, pady=10)
        self.lbl_rw = tk.Label(rw, text="🎉 点击右侧按钮，为优秀工程师签发鲁班奖激励绩效！", font=("Microsoft YaHei", 11, "bold"), bg="#FFFBEB", wraplength=550)
        self.lbl_rw.pack(side="left")
        def draw(): self.lbl_rw.configure(text=random.choice(self.rewards), fg=self.C_GOLD)
        self.create_btn(rw, "🎁 抽取节点奖", self.C_GOLD, draw).pack(side="right")
        self.create_btn(self.root, "🔄 滚动滚动招标", self.C_PRIMARY, self.setup_start_screen).pack(pady=30)
if __name__ == "__main__":
    root = tk.Tk(); app = PM_LeanSandtable(root); root.mainloop()
