import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

import customtkinter as ctk
from database import ShopDatabase


# =========================================================
# НАСТРОЙКИ И ЦВЕТОВАЯ ПАЛИТРА
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#151720"
SIDEBAR = "#1B1E2A"
PANEL = "#202432"
CARD = "#272C3D"
CARD_HOVER = "#30364A"

TEXT = "#F0F0F7"
MUTED = "#9DA5BC"

LAVENDER = "#B8B5F2"
LAVENDER_HOVER = "#A29FE3"

MINT = "#A9D6C3"
PEACH = "#E8B7AD"
PINK = "#D9A9C8"

BORDER = "#373D52"
FONT = "Segoe UI"


# =========================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# =========================================================

class ShopApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.db = ShopDatabase()

        self.title("Atelier — пространство магазина")
        self.geometry("1240x820")
        self.minsize(920, 680)
        self.configure(fg_color=BG)

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.search_var = tk.StringVar()
        self.search_after = None
        self.toast_after = None
        self.toast = None
        self.current_view = "catalog"

        self.build_layout()
        self.refresh_products()

    # =====================================================
    # ОСНОВНОЙ ИНТЕРФЕЙС
    # =====================================================

    def build_layout(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель
        self.sidebar = ctk.CTkFrame(
            self,
            width=218,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # Логотип и название
        brand = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        brand.pack(
            fill="x",
            padx=22,
            pady=(27, 35)
        )

        logo = ctk.CTkLabel(
            brand,
            text="a.",
            width=42,
            height=42,
            corner_radius=14,
            fg_color=LAVENDER,
            text_color=BG,
            font=(FONT, 25, "bold")
        )

        logo.pack(
            anchor="w",
            pady=(0, 13)
        )

        ctk.CTkLabel(
            brand,
            text="ATELIER",
            font=(FONT, 15, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="STORE MANAGEMENT",
            font=(FONT, 8, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # Навигация
        ctk.CTkLabel(
            self.sidebar,
            text="РАБОЧЕЕ ПРОСТРАНСТВО",
            font=(FONT, 9, "bold"),
            text_color="#727B95"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 12)
        )

        self.nav_catalog = self.nav_button(
            "▦",
            "Каталог товаров",
            self.show_catalog,
            selected=True
        )

        self.nav_catalog.pack(
            fill="x",
            padx=12,
            pady=3
        )

        self.nav_add = self.nav_button(
            "＋",
            "Добавить товар",
            self.open_add_dialog
        )

        self.nav_add.pack(
            fill="x",
            padx=12,
            pady=3
        )

        # Разделитель
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=BORDER
        ).pack(
            fill="x",
            padx=20,
            pady=22
        )

        # Декоративный блок
        ctk.CTkLabel(
            self.sidebar,
            text="ПОДСКАЗКА",
            font=(FONT, 9, "bold"),
            text_color="#727B95"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 9)
        )

        tip = ctk.CTkFrame(
            self.sidebar,
            fg_color="#25283A",
            corner_radius=14
        )

        tip.pack(
            fill="x",
            padx=13
        )

        ctk.CTkLabel(
            tip,
            text="✦",
            font=(FONT, 20),
            text_color=PINK
        ).pack(
            anchor="w",
            padx=13,
            pady=(12, 0)
        )

        ctk.CTkLabel(
            tip,
            text="Маленькие детали\nсоздают большой\nпорядок.",
            font=(FONT, 11),
            text_color=TEXT,
            justify="left"
        ).pack(
            anchor="w",
            padx=13,
            pady=(4, 14)
        )

        # Статус базы данных внизу
        bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=22
        )

        ctk.CTkLabel(
            bottom,
            text="●  БАЗА ДАННЫХ ONLINE",
            font=(FONT, 9, "bold"),
            text_color=MINT
        ).pack(anchor="w")

        ctk.CTkLabel(
            bottom,
            text="SQLite · локальное хранение",
            font=(FONT, 9),
            text_color=MUTED
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # Правая рабочая область
        self.content = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        self.content.grid_rowconfigure(
            3,
            weight=1
        )

        self.build_topbar()
        self.build_hero()
        self.build_stats()
        self.build_catalog_area()

    # =====================================================
    # КНОПКИ БОКОВОЙ ПАНЕЛИ
    # =====================================================

    def nav_button(
        self,
        icon,
        label,
        command,
        selected=False
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=f"{icon}    {label}",
            command=command,
            height=43,
            corner_radius=11,
            anchor="w",
            fg_color="#303149" if selected else "transparent",
            hover_color="#2B2F43",
            text_color=LAVENDER if selected else MUTED,
            font=(
                FONT,
                12,
                "bold" if selected else "normal"
            )
        )

        return button

    # =====================================================
    # ВЕРХНЯЯ ПАНЕЛЬ
    # =====================================================

    def build_topbar(self):

        top = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=32,
            pady=(22, 12)
        )

        top.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            top,
            text="ПАНЕЛЬ УПРАВЛЕНИЯ   /   МАГАЗИН",
            font=(FONT, 10, "bold"),
            text_color=MUTED
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.date_label = ctk.CTkLabel(
            top,
            text="●  Рабочее пространство",
            font=(FONT, 10, "bold"),
            text_color=MINT,
            fg_color="#222E31",
            corner_radius=10
        )

        self.date_label.grid(
            row=0,
            column=1,
            sticky="e",
            ipadx=12,
            ipady=8
        )

    # =====================================================
    # ДЕКОРАТИВНЫЙ БАННЕР
    # =====================================================

    def build_hero(self):

        hero = ctk.CTkFrame(
            self.content,
            fg_color="#292A40",
            corner_radius=20,
            border_width=1,
            border_color="#3D3D5B"
        )

        hero.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=32,
            pady=(4, 18)
        )

        hero.grid_columnconfigure(
            0,
            weight=1
        )

        left = ctk.CTkFrame(
            hero,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=23
        )

        ctk.CTkLabel(
            left,
            text="ТВОЙ МАГАЗИН — ПОД КОНТРОЛЕМ",
            font=(FONT, 9, "bold"),
            text_color=PINK
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Всё на своих местах.",
            font=(FONT, 25, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            pady=(7, 4)
        )

        ctk.CTkLabel(
            left,
            text=(
                "Управляй ассортиментом, следи за остатками "
                "и обновляй цены."
            ),
            font=(FONT, 11),
            text_color="#B8BCD0"
        ).pack(anchor="w")

        self.create_button(
            hero,
            "＋  Новая позиция",
            self.open_add_dialog,
            primary=True
        ).grid(
            row=0,
            column=1,
            padx=24,
            pady=24,
            sticky="e"
        )

        # Декоративный символ
        deco = ctk.CTkFrame(
            hero,
            fg_color="transparent",
            width=5
        )

        deco.grid(
            row=0,
            column=2,
            padx=(0, 16)
        )

        ctk.CTkLabel(
            deco,
            text="✳",
            font=(FONT, 39),
            text_color="#8E8BC6"
        ).pack()

    # =====================================================
    # КАРТОЧКИ СТАТИСТИКИ
    # =====================================================

    def build_stats(self):

        self.stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.stats.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=27,
            pady=(0, 16)
        )

        self.stats.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.stat_products = self.stat_card(
            self.stats,
            0,
            "ТОВАРНЫЕ ПОЗИЦИИ",
            "0",
            "▦",
            LAVENDER
        )

        self.stat_quantity = self.stat_card(
            self.stats,
            1,
            "ЕДИНИЦ НА СКЛАДЕ",
            "0",
            "↗",
            MINT
        )

        self.stat_value = self.stat_card(
            self.stats,
            2,
            "СТОИМОСТЬ ОСТАТКОВ",
            "0 ₽",
            "◇",
            PINK
        )

    def stat_card(
        self,
        parent,
        column,
        title,
        value,
        icon,
        color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=15,
            border_width=1,
            border_color="#292E3E"
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=(FONT, 20, "bold"),
            text_color=color
        ).grid(
            row=0,
            column=1,
            sticky="e",
            padx=15,
            pady=(13, 0)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=(FONT, 9, "bold"),
            text_color=MUTED
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(16, 0)
        )

        result = ctk.CTkLabel(
            card,
            text=value,
            font=(FONT, 23, "bold"),
            text_color=TEXT
        )

        result.grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=(5, 15)
        )

        return result

    # =====================================================
    # КАТАЛОГ И ПОИСК
    # =====================================================

    def build_catalog_area(self):

        section = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        section.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=32,
            pady=(0, 24)
        )

        section.grid_columnconfigure(
            0,
            weight=1
        )

        section.grid_rowconfigure(
            2,
            weight=1
        )

        # Заголовок каталога
        heading = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )

        heading.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        heading.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            heading,
            text="Твой каталог",
            font=(FONT, 19, "bold"),
            text_color=TEXT
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            heading,
            text="КАРТОЧКИ ТОВАРОВ",
            font=(FONT, 9, "bold"),
            text_color=MUTED
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # Панель поиска
        toolbar = ctk.CTkFrame(
            section,
            fg_color="transparent"
        )

        toolbar.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        toolbar.grid_columnconfigure(
            0,
            weight=1
        )

        search_shell = ctk.CTkFrame(
            toolbar,
            fg_color=CARD,
            corner_radius=11
        )

        search_shell.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            search_shell,
            text="⌕",
            font=(FONT, 22),
            text_color=LAVENDER
        ).pack(
            side="left",
            padx=(12, 6)
        )

        self.search_entry = ctk.CTkEntry(
            search_shell,
            textvariable=self.search_var,
            placeholder_text="Поиск по названию товара...",
            height=38,
            border_width=0,
            fg_color="transparent",
            text_color=TEXT,
            placeholder_text_color=MUTED,
            font=(FONT, 12)
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.search_var.trace_add(
            "write",
            self.on_search_change
        )

        self.result_label = ctk.CTkLabel(
            toolbar,
            text="0 результатов",
            font=(FONT, 10),
            text_color=MUTED
        )

        self.result_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # Прокручиваемый каталог
        self.catalog = ctk.CTkScrollableFrame(
            section,
            fg_color=PANEL,
            corner_radius=17,
            scrollbar_button_color="#505775",
            scrollbar_button_hover_color=LAVENDER
        )

        self.catalog.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.catalog.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
            uniform="cards"
        )

    # =====================================================
    # СОЗДАНИЕ СОВРЕМЕННЫХ КНОПОК
    # =====================================================

    def create_button(
        self,
        parent,
        text,
        command,
        primary=False,
        danger=False
    ):

        if danger:
            fg = PEACH
            hover = "#D99F95"
            color = BG

        elif primary:
            fg = LAVENDER
            hover = LAVENDER_HOVER
            color = BG

        else:
            fg = CARD
            hover = CARD_HOVER
            color = TEXT

        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=39,
            corner_radius=11,
            fg_color=fg,
            hover_color=hover,
            text_color=color,
            font=(FONT, 11, "bold")
        )

    # =====================================================
    # ПОИСК С ЗАДЕРЖКОЙ
    # =====================================================

    def on_search_change(self, *_):

        if self.search_after is not None:
            self.after_cancel(self.search_after)

        self.search_after = self.after(
            180,
            self.refresh_products
        )

    def show_catalog(self):

        self.current_view = "catalog"

        self.nav_catalog.configure(
            fg_color="#303149",
            text_color=LAVENDER
        )

        self.nav_add.configure(
            fg_color="transparent",
            text_color=MUTED
        )

        self.search_entry.focus_set()

    # =====================================================
    # ОБНОВЛЕНИЕ КАТАЛОГА
    # =====================================================

    def refresh_products(self):

        self.search_after = None

        for child in self.catalog.winfo_children():
            child.destroy()

        try:
            products = self.db.get_products(
                self.search_var.get()
            )

            stats = self.db.get_statistics()

        except Exception as error:
            self.show_toast(
                f"Ошибка базы данных: {error}"
            )
            return

        # Обновление статистики
        self.stat_products.configure(
            text=str(stats["product_count"])
        )

        self.stat_quantity.configure(
            text=str(stats["total_quantity"])
        )

        self.stat_value.configure(
            text=self.money(stats["total_value"])
        )

        self.result_label.configure(
            text=f"{len(products)} результатов"
        )

        # Пустой каталог
        if not products:

            empty = ctk.CTkFrame(
                self.catalog,
                fg_color="transparent"
            )

            empty.grid(
                row=0,
                column=0,
                columnspan=3,
                pady=55
            )

            ctk.CTkLabel(
                empty,
                text="✳",
                font=(FONT, 38),
                text_color="#77749F"
            ).pack()

            if self.search_var.get().strip():
                title = "Ничего не нашлось"
                subtitle = "Попробуй изменить поисковый запрос."

            else:
                title = "Здесь пока тихо"
                subtitle = "Добавь первую позицию — и каталог оживёт."

            ctk.CTkLabel(
                empty,
                text=title,
                font=(FONT, 17, "bold"),
                text_color=TEXT
            ).pack(pady=(8, 4))

            ctk.CTkLabel(
                empty,
                text=subtitle,
                font=(FONT, 11),
                text_color=MUTED
            ).pack()

            if not self.search_var.get().strip():

                self.create_button(
                    empty,
                    "＋  Добавить первый товар",
                    self.open_add_dialog,
                    primary=True
                ).pack(pady=15)

            return

        # Распределение товаров по сетке
        for index, product in enumerate(products):

            row = index // 3
            column = index % 3

            self.create_product_card(
                product,
                row,
                column
            )

    # =====================================================
    # КАРТОЧКА ТОВАРА
    # =====================================================

    def create_product_card(
        self,
        product,
        row,
        column
    ):

        card = ctk.CTkFrame(
            self.catalog,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8
        )

        # Эффект при наведении
        def hover_on(event):
            card.configure(
                fg_color=CARD_HOVER,
                border_color="#555878"
            )

        def hover_off(event):
            card.configure(
                fg_color=CARD,
                border_color=BORDER
            )

        card.bind("<Enter>", hover_on)
        card.bind("<Leave>", hover_off)

        # Верхняя часть карточки
        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(14, 3)
        )

        ctk.CTkLabel(
            top,
            text="✧",
            font=(FONT, 26),
            text_color=LAVENDER
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=f"№ {product['id']:04d}",
            font=(FONT, 9, "bold"),
            text_color=MUTED
        ).pack(side="right")

        # Название
        ctk.CTkLabel(
            card,
            text=product["name"],
            font=(FONT, 15, "bold"),
            text_color=TEXT,
            wraplength=230,
            justify="left"
        ).pack(
            anchor="w",
            padx=16,
            pady=(7, 4)
        )

        # Цена
        ctk.CTkLabel(
            card,
            text=self.money(product["price"]),
            font=(FONT, 22, "bold"),
            text_color=MINT
        ).pack(
            anchor="w",
            padx=16,
            pady=(3, 5)
        )

        # Остаток товара
        quantity = product["quantity"]

        if quantity == 0:
            stock = "●  Нет в наличии"
            color = PEACH

        elif quantity <= 5:
            stock = f"●  Заканчивается · {quantity} шт."
            color = "#E7C38E"

        else:
            stock = f"●  На складе · {quantity} шт."
            color = MINT

        ctk.CTkLabel(
            card,
            text=stock,
            font=(FONT, 10, "bold"),
            text_color=color
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 13)
        )

        # Кнопки управления
        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            padx=11,
            pady=(0, 12)
        )

        actions.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.create_button(
            actions,
            "Редактировать",
            lambda item=product: self.open_edit_dialog(item)
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=3
        )

        self.create_button(
            actions,
            "Удалить",
            lambda item=product: self.delete_product(item),
            danger=True
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=3
        )

    # =====================================================
    # ПОЛЯ ВВОДА
    # =====================================================

    def create_input(
        self,
        parent,
        label,
        placeholder
    ):

        ctk.CTkLabel(
            parent,
            text=label,
            font=(FONT, 11, "bold"),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(8, 5)
        )

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=40,
            corner_radius=10,
            fg_color=PANEL,
            border_color=BORDER,
            text_color=TEXT,
            placeholder_text_color=MUTED,
            font=(FONT, 12)
        )

        entry.pack(
            fill="x",
            padx=25
        )

        return entry

    # =====================================================
    # ДОБАВЛЕНИЕ ТОВАРА
    # =====================================================

    def open_add_dialog(self):

        self.nav_add.configure(
            fg_color="#303149",
            text_color=LAVENDER
        )

        dialog = ctk.CTkToplevel(self)

        dialog.title("Новая позиция")
        dialog.geometry("440x465")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG)

        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Добавим что-нибудь новое",
            font=(FONT, 21, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(24, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Заполни информацию о товаре",
            font=(FONT, 11),
            text_color=MUTED
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 12)
        )

        name = self.create_input(
            dialog,
            "Название",
            "Например, Ароматическая свеча"
        )

        price = self.create_input(
            dialog,
            "Цена в рублях",
            "Например, 890.00"
        )

        quantity = self.create_input(
            dialog,
            "Количество",
            "Например, 12"
        )

        def save():

            title = name.get().strip()

            if not title:
                self.show_toast(
                    "Название не должно быть пустым"
                )
                return

            try:
                amount = self.parse_price(
                    price.get()
                )

                count = int(
                    quantity.get().strip()
                )

                if count < 0:
                    raise ValueError

            except (ValueError, InvalidOperation):
                self.show_toast(
                    "Проверь цену и количество"
                )
                return

            try:
                self.db.add_product(
                    title,
                    amount,
                    count
                )

            except Exception as error:
                self.show_toast(
                    f"Не удалось сохранить: {error}"
                )
                return

            dialog.destroy()

            self.refresh_products()

            self.show_toast(
                "✦  Новая позиция добавлена"
            )

        self.create_button(
            dialog,
            "Сохранить позицию",
            save,
            primary=True
        ).pack(
            fill="x",
            padx=25,
            pady=22
        )

    # =====================================================
    # РЕДАКТИРОВАНИЕ ТОВАРА
    # =====================================================

    def open_edit_dialog(self, product):

        dialog = ctk.CTkToplevel(self)

        dialog.title("Редактирование позиции")
        dialog.geometry("440x400")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG)

        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Настроить позицию",
            font=(FONT, 21, "bold"),
            text_color=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(24, 5)
        )

        ctk.CTkLabel(
            dialog,
            text=f"#{product['id']}  ·  {product['name']}",
            font=(FONT, 11),
            text_color=MUTED,
            wraplength=380
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        price = self.create_input(
            dialog,
            "Цена в рублях",
            "Новая цена"
        )

        price.insert(
            0,
            str(product["price"])
        )

        quantity = self.create_input(
            dialog,
            "Количество на складе",
            "Новое количество"
        )

        quantity.insert(
            0,
            str(product["quantity"])
        )

        def save():

            try:
                amount = self.parse_price(
                    price.get()
                )

                count = int(
                    quantity.get().strip()
                )

                if count < 0:
                    raise ValueError

            except (ValueError, InvalidOperation):
                self.show_toast(
                    "Введи цену ≥ 0 и целое количество ≥ 0"
                )
                return

            try:
                self.db.update_price(
                    product["id"],
                    amount
                )

                self.db.update_quantity(
                    product["id"],
                    count
                )

            except Exception as error:
                self.show_toast(
                    f"Ошибка сохранения: {error}"
                )
                return

            dialog.destroy()

            self.refresh_products()

            self.show_toast(
                "Изменения сохранены"
            )

        self.create_button(
            dialog,
            "Сохранить изменения",
            save,
            primary=True
        ).pack(
            fill="x",
            padx=25,
            pady=22
        )

    # =====================================================
    # УДАЛЕНИЕ ТОВАРА
    # =====================================================

    def delete_product(self, product):

        answer = messagebox.askyesno(
            "Удаление позиции",
            f"Удалить «{product['name']}» из каталога?",
            parent=self
        )

        if not answer:
            return

        try:
            deleted = self.db.delete_product(
                product["id"]
            )

        except Exception as error:
            self.show_toast(
                f"Ошибка удаления: {error}"
            )
            return

        if deleted:
            self.refresh_products()
            self.show_toast("Позиция удалена")

        else:
            self.show_toast(
                "Эта позиция уже удалена"
            )

    # =====================================================
    # ФОРМАТИРОВАНИЕ ЦЕНЫ
    # =====================================================

    @staticmethod
    def parse_price(value):

        amount = Decimal(
            value.strip()
            .replace(" ", "")
            .replace(",", ".")
        )

        if not amount.is_finite() or amount < 0:
            raise ValueError

        return float(amount)

    @staticmethod
    def money(value):

        formatted = f"{value:,.2f}"

        formatted = formatted.replace(",", " ")
        formatted = formatted.replace(".", ",")

        return f"{formatted} ₽"

    # =====================================================
    # ВСПЛЫВАЮЩИЕ УВЕДОМЛЕНИЯ
    # =====================================================

    def show_toast(self, text):

        if self.toast_after is not None:
            try:
                self.after_cancel(
                    self.toast_after
                )
            except tk.TclError:
                pass

        if self.toast is not None:
            self.toast.destroy()

        self.toast = ctk.CTkLabel(
            self,
            text=text,
            fg_color="#3A3B55",
            text_color=TEXT,
            corner_radius=12,
            font=(FONT, 12, "bold"),
            padx=18,
            pady=12
        )

        self.toast.place(
            relx=0.985,
            rely=0.975,
            anchor="se"
        )

        self.toast_after = self.after(
            2400,
            self.hide_toast
        )

    def hide_toast(self):

        self.toast_after = None

        if self.toast is not None:
            self.toast.destroy()
            self.toast = None

    # =====================================================
    # ЗАКРЫТИЕ ПРИЛОЖЕНИЯ
    # =====================================================

    def close_app(self):

        if self.search_after is not None:
            try:
                self.after_cancel(
                    self.search_after
                )
            except tk.TclError:
                pass

        if self.toast_after is not None:
            try:
                self.after_cancel(
                    self.toast_after
                )
            except tk.TclError:
                pass

        self.db.close()
        self.destroy()


# =========================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# =========================================================

if __name__ == "__main__":

    app = ShopApp()
    app.mainloop()