# -*- coding: utf-8 -*-
"""
BATNA - Calculadora de negociación (ZOPA, Litigio y Comercial)

Autor: Ing. Norberto Hernández
Cédula profesional: 15061201
Cipher · Sistemas computacionales IoT
Arandas, Jalisco

Interfaz rediseñada con la identidad visual de la tarjeta de presentación Cipher.
Recursos gráficos en la carpeta "assets/" (junto a este archivo):
    - logo_cipher.png  (logo circular)
    - qr_cipher.png    (código QR de la tarjeta)
    - serif_bold.ttf   (tipografía serif en negrita, como la tarjeta)
"""
import os
import json
import random
from datetime import datetime

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.metrics import dp, sp
from kivy.properties import BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import escape_markup

# ----------------------------------------------------------------------
#  AUTORÍA
# ----------------------------------------------------------------------
__author__ = "Ing. Norberto Hernández"
__license_professional__ = "Cédula profesional 15061201"

AUTOR = "Ing. Norberto Hernández"
CEDULA = "15061201"
EMPRESA = "Cipher"
GIRO = "Sistemas computacionales IoT"
WHATSAPP = "3481959549"
UBICACION = "Arandas, Jalisco"

# ----------------------------------------------------------------------
#  RECURSOS
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
RUTA_LOGO = os.path.join(ASSETS, "logo_cipher.png")
RUTA_QR = os.path.join(ASSETS, "qr_cipher.png")
RUTA_FUENTE = os.path.join(ASSETS, "serif_bold.ttf")

ARCHIVO_HISTORIAL = "historial_batna.json"

# Tipografía serif en negrita (como la tarjeta); si no existe, usa Roboto
FUENTE = "Roboto"
if os.path.exists(RUTA_FUENTE):
    LabelBase.register(
        name="CipherSerif",
        fn_regular=RUTA_FUENTE,
        fn_bold=RUTA_FUENTE,
    )
    FUENTE = "CipherSerif"

# ----------------------------------------------------------------------
#  PALETA (tomada de la tarjeta y del logo Cipher)
# ----------------------------------------------------------------------
CIAN = (0.10, 0.78, 0.98, 1)
AZUL = (0.35, 0.42, 0.98, 1)
MAGENTA = (0.74, 0.30, 0.92, 1)
TEXTO = (0.05, 0.05, 0.09, 1)
BLANCO = (1, 1, 1, 1)
VERDE_HEX = "1b8f4a"
ROJO_HEX = "c62828"
VIOLETA_HEX = "5a3fd8"

_cache_texturas = {}


def degradado(colores, horizontal=True, n=128):
    """Textura de degradado multi-color (se crea una sola vez)."""
    clave = (tuple(tuple(c) for c in colores), horizontal)
    if clave in _cache_texturas:
        return _cache_texturas[clave]

    tex = Texture.create(size=(n, 1) if horizontal else (1, n), colorfmt="rgba")
    buf = bytearray()
    tramos = len(colores) - 1
    for i in range(n):
        t = i / (n - 1)
        k = min(int(t * tramos), tramos - 1)
        u = t * tramos - k
        a, b = colores[k], colores[k + 1]
        buf.extend(int((a[j] + (b[j] - a[j]) * u) * 255) for j in range(4))
    tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
    tex.mag_filter = "linear"
    tex.min_filter = "linear"
    _cache_texturas[clave] = tex
    return tex


def degradado_cipher():
    # cian -> azul -> magenta (colores del logo)
    return degradado([CIAN, AZUL, MAGENTA], horizontal=True)


# ----------------------------------------------------------------------
#  HISTORIAL (sin cambios de lógica)
# ----------------------------------------------------------------------
def guardar_en_historial(tipo_analisis, datos_resultado):
    historial = []
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except Exception:
            historial = []

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo_analisis,
        "resultado": datos_resultado,
    }
    historial.append(registro)

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)


# ----------------------------------------------------------------------
#  WIDGETS CON EL ESTILO DE LA TARJETA
# ----------------------------------------------------------------------
class FondoCircuito(Widget):
    """Fondo lavanda-azul con líneas de circuito, como la tarjeta."""

    def __init__(self, **kw):
        super().__init__(**kw)
        rng = random.Random(2026)  # semilla fija: el diseño no cambia
        self._trazos = []
        for _ in range(28):
            x, y = rng.random(), rng.random()
            pts = [(x, y)]
            for _ in range(rng.randint(2, 4)):
                dx = rng.choice([-1, 0, 1]) * rng.uniform(0.05, 0.18)
                dy = rng.choice([-1, 0, 1]) * rng.uniform(0.03, 0.12)
                if dx == 0 and dy == 0:
                    dx = 0.08
                x = min(max(x + dx, 0), 1)
                y = min(max(y + dy, 0), 1)
                pts.append((x, y))
            self._trazos.append(pts)
        self.bind(pos=self._dibujar, size=self._dibujar)

    def _dibujar(self, *args):
        self.canvas.clear()
        x0, y0 = self.pos
        w, h = self.size
        fondo = degradado(
            [(0.70, 0.79, 0.99, 1), (0.82, 0.85, 0.99, 1), (0.94, 0.93, 1.0, 1)],
            horizontal=False,
        )
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size, texture=fondo)
            for pts in self._trazos:
                coords = []
                for px, py in pts:
                    coords.extend([x0 + px * w, y0 + py * h])
                Color(0.30, 0.78, 0.98, 0.40)
                Line(points=coords, width=dp(1.4))
                ex, ey = coords[-2], coords[-1]
                Color(0.30, 0.78, 0.98, 0.65)
                Line(circle=(ex, ey, dp(4)), width=dp(1.2))
                Ellipse(pos=(ex - dp(1.5), ey - dp(1.5)), size=(dp(3), dp(3)))


class Tarjeta(BoxLayout):
    """Panel blanco redondeado con borde cian. Ajusta su alto al contenido."""

    def __init__(self, auto=True, **kw):
        base = dict(orientation="vertical", padding=dp(14), spacing=dp(10))
        if auto:
            base["size_hint_y"] = None
        base.update(kw)
        super().__init__(**base)
        if auto:
            self.bind(minimum_height=self.setter("height"))
        with self.canvas.before:
            Color(1, 1, 1, 0.88)
            self._bg = RoundedRectangle(radius=[dp(18)])
            Color(*CIAN[:3], 0.9)
            self._borde = Line(width=dp(1.2))
        self.bind(pos=self._actualizar, size=self._actualizar)

    def _actualizar(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._borde.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(18))


class Texto(Label):
    """Label serif negrita que ajusta su alto al texto (con markup)."""

    def __init__(self, **kw):
        base = dict(
            font_name=FUENTE,
            color=TEXTO,
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=True,
            font_size=sp(16),
        )
        base.update(kw)
        super().__init__(**base)
        self.bind(width=self._ajustar, texture_size=self._ajustar)

    def _ajustar(self, *args):
        self.text_size = (self.width, None)
        self.height = self.texture_size[1] + dp(4)


def titulo(texto, tam=21, **kw):
    """Título con halo blanco, como el texto de la tarjeta."""
    return Texto(
        text=texto,
        font_size=sp(tam),
        bold=True,
        outline_width=dp(2),
        outline_color=(1, 1, 1, 1),
        **kw,
    )


class CampoCipher(TextInput):
    """Campo de texto redondeado con borde cian (azul al enfocar)."""

    def __init__(self, **kw):
        base = dict(
            multiline=False,
            background_normal="",
            background_active="",
            background_color=(0, 0, 0, 0),
            foreground_color=TEXTO,
            hint_text_color=(0.38, 0.40, 0.58, 1),
            cursor_color=AZUL,
            selection_color=(0.2, 0.8, 0.98, 0.35),
            size_hint_y=None,
            height=dp(46),
            padding=[dp(14), dp(12), dp(14), dp(8)],
            font_name=FUENTE,
            font_size=sp(16),
        )
        base.update(kw)
        super().__init__(**base)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self._bg = RoundedRectangle(radius=[dp(14)])
            self._color_borde = Color(*CIAN)
            self._borde = Line(width=dp(1.2))
        self.bind(pos=self._actualizar, size=self._actualizar, focus=self._actualizar)
        self._actualizar()

    def _actualizar(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._borde.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(14))
        if self.focus:
            self._color_borde.rgba = AZUL
            self._borde.width = dp(1.8)
        else:
            self._color_borde.rgba = CIAN
            self._borde.width = dp(1.2)


class BotonCipher(ButtonBehavior, Label):
    """Botón con degradado cian → azul → magenta (colores del logo)."""

    def __init__(self, **kw):
        base = dict(
            font_name=FUENTE,
            bold=True,
            font_size=sp(17),
            color=BLANCO,
            size_hint_y=None,
            height=dp(50),
        )
        base.update(kw)
        super().__init__(**base)
        with self.canvas.before:
            self._tinte = Color(1, 1, 1, 1)
            self._bg = RoundedRectangle(texture=degradado_cipher(), radius=[dp(25)])
        self.bind(pos=self._actualizar, size=self._actualizar, state=self._estado)

    def _actualizar(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def _estado(self, *args):
        self._tinte.rgba = (0.78, 0.78, 0.78, 1) if self.state == "down" else (1, 1, 1, 1)


class Pestana(ButtonBehavior, Label):
    """Pestaña en forma de píldora; activa = degradado, inactiva = blanca."""

    activa = BooleanProperty(False)

    def __init__(self, **kw):
        base = dict(
            font_name=FUENTE,
            bold=True,
            font_size=sp(12),
            size_hint_y=None,
            height=dp(40),
        )
        base.update(kw)
        super().__init__(**base)
        with self.canvas.before:
            self._tinte = Color(1, 1, 1, 0.75)
            self._bg = RoundedRectangle(radius=[dp(20)])
        self.bind(pos=self._actualizar, size=self._actualizar, activa=self._actualizar)
        self._actualizar()

    def _actualizar(self, *args):
        self._bg.pos = self.pos
        self._bg.size = self.size
        if self.activa:
            self._tinte.rgba = (1, 1, 1, 1)
            self._bg.texture = degradado_cipher()
            self.color = BLANCO
        else:
            self._tinte.rgba = (1, 1, 1, 0.75)
            self._bg.texture = None
            self.color = TEXTO


# ----------------------------------------------------------------------
#  PANEL PRINCIPAL
# ----------------------------------------------------------------------
class CalculadoraPanel(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(FondoCircuito())

        raiz = BoxLayout(
            orientation="vertical", padding=[dp(10), dp(8)], spacing=dp(8)
        )
        raiz.add_widget(self.crear_encabezado())

        # Pantallas
        self.sm = ScreenManager(transition=FadeTransition(duration=0.12))
        self._agregar_pantalla("zopa", self.crear_vista_zopa())
        self._agregar_pantalla("litigio", self.crear_vista_litigio())
        self._agregar_pantalla("comercial", self.crear_vista_comercial())
        self._agregar_pantalla("historial", self.crear_vista_historial())
        self._agregar_pantalla("autor", self.crear_vista_autor())

        raiz.add_widget(self.crear_barra_pestanas())
        raiz.add_widget(self.sm)
        raiz.add_widget(self.crear_pie())
        self.add_widget(raiz)

        self.ir_a("zopa")

    # --- estructura ----------------------------------------------------
    def _agregar_pantalla(self, nombre, contenido):
        pantalla = Screen(name=nombre)
        pantalla.add_widget(contenido)
        self.sm.add_widget(pantalla)

    def crear_encabezado(self):
        fila = BoxLayout(size_hint_y=None, height=dp(84), spacing=dp(12))
        if os.path.exists(RUTA_LOGO):
            fila.add_widget(
                Image(source=RUTA_LOGO, size_hint=(None, 1), width=dp(84))
            )

        textos = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        textos.bind(minimum_height=textos.setter("height"))
        textos.add_widget(titulo("Calculadora BATNA", tam=23))
        textos.add_widget(titulo(GIRO, tam=14))
        textos.add_widget(titulo(AUTOR, tam=13))

        centro = AnchorLayout(anchor_x="left", anchor_y="center")
        centro.add_widget(textos)
        fila.add_widget(centro)
        return fila

    def crear_barra_pestanas(self):
        barra = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(6))
        self.pestanas = {}
        for nombre, texto in [
            ("zopa", "ZOPA"),
            ("litigio", "Litigio"),
            ("comercial", "Comercial"),
            ("historial", "Historial"),
            ("autor", "Autor"),
        ]:
            pestana = Pestana(text=texto)
            pestana.bind(on_release=lambda inst, n=nombre: self.ir_a(n))
            self.pestanas[nombre] = pestana
            barra.add_widget(pestana)
        return barra

    def crear_pie(self):
        pie = Tarjeta(padding=[dp(10), dp(6)], spacing=dp(1))
        pie.add_widget(
            Texto(
                text=f"Desarrollado por [b]{AUTOR}[/b]",
                font_size=sp(12),
                halign="center",
            )
        )
        pie.add_widget(
            Texto(
                text=f"Cédula Prof. {CEDULA} · {EMPRESA} · {UBICACION}",
                font_size=sp(11),
                halign="center",
            )
        )
        return pie

    def ir_a(self, nombre):
        self.sm.current = nombre
        for n, pestana in self.pestanas.items():
            pestana.activa = n == nombre

    # --- constructor genérico de formularios ---------------------------
    def _formulario(self, titulo_txt, campos, texto_boton, accion, mensaje_inicial):
        """campos: lista de (nombre_atributo, hint_text)."""
        caja = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(12),
            padding=[0, dp(4)],
        )
        caja.bind(minimum_height=caja.setter("height"))

        tarjeta = Tarjeta()
        tarjeta.add_widget(titulo(titulo_txt))
        for atributo, hint in campos:
            campo = CampoCipher(hint_text=hint, input_filter="float")
            setattr(self, atributo, campo)
            tarjeta.add_widget(campo)
        boton = BotonCipher(text=texto_boton)
        boton.bind(on_release=accion)
        tarjeta.add_widget(boton)

        resultado = Tarjeta()
        etiqueta = Texto(text=mensaje_inicial, halign="center", font_size=sp(17))
        resultado.add_widget(etiqueta)

        caja.add_widget(tarjeta)
        caja.add_widget(resultado)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(caja)
        return scroll, etiqueta

    # --- PESTAÑA ZOPA --------------------------------------------------
    def crear_vista_zopa(self):
        vista, self.lbl_res_zopa = self._formulario(
            "Análisis de ZOPA",
            [
                ("input_vendedor", "Reserva Vendedor ($)"),
                ("input_comprador", "Reserva Comprador ($)"),
            ],
            "Calcular ZOPA",
            self.calcular_zopa,
            "Introduce los datos y presiona calcular.",
        )
        return vista

    def calcular_zopa(self, instance):
        try:
            vendedor = float(self.input_vendedor.text)
            comprador = float(self.input_comprador.text)

            if comprador >= vendedor:
                excedente = comprador - vendedor
                res = (
                    f"[b][color={VERDE_HEX}]ZOPA Viable[/color][/b]\n"
                    f"Rango: ${vendedor:,.2f} a ${comprador:,.2f}\n"
                    f"Excedente: ${excedente:,.2f}"
                )
                guardar_en_historial("ZOPA", {"reserva_vendedor": vendedor, "reserva_comprador": comprador, "viable": True, "excedente": excedente})
            else:
                brecha = vendedor - comprador
                res = (
                    f"[b][color={ROJO_HEX}]NO Existe ZOPA[/color][/b]\n"
                    f"Brecha: ${brecha:,.2f}\n"
                    f"Consejo: Detén la negociación y ejecuta tu BATNA."
                )
                guardar_en_historial("ZOPA", {"reserva_vendedor": vendedor, "reserva_comprador": comprador, "viable": False, "brecha": brecha})

            self.lbl_res_zopa.text = res
        except ValueError:
            self.lbl_res_zopa.text = f"[color={ROJO_HEX}]Error: Introduce números válidos.[/color]"

    # --- PESTAÑA LITIGIO -----------------------------------------------
    def crear_vista_litigio(self):
        vista, self.lbl_res_litigio = self._formulario(
            "BATNA en Litigios",
            [
                ("input_monto_litigio", "Monto en disputa ($)"),
                ("input_prob_ganar", "Probabilidad de ganar (0 a 100 %)"),
                ("input_gastos_legales", "Gastos legales estimados ($)"),
            ],
            "Calcular Valor Estimado",
            self.calcular_litigio,
            "Resultados...",
        )
        return vista

    def calcular_litigio(self, instance):
        try:
            monto = float(self.input_monto_litigio.text)
            prob_ganar = float(self.input_prob_ganar.text) / 100.0
            gastos = float(self.input_gastos_legales.text)

            prob_perder = 1.0 - prob_ganar
            neto_ganar = monto - gastos
            neto_perder = -gastos
            valor_estimado = (prob_ganar * neto_ganar) + (prob_perder * neto_perder)

            res = (
                f"Escenario Victoria ({prob_ganar*100:.1f}%): ${neto_ganar:,.2f}\n"
                f"Escenario Derrota ({prob_perder*100:.1f}%): ${neto_perder:,.2f}\n"
                f"[b][color={VIOLETA_HEX}]VALOR ESTIMADO BATNA: ${valor_estimado:,.2f}[/color][/b]"
            )

            guardar_en_historial("Litigio", {"monto_disputa": monto, "probabilidad_ganar": prob_ganar, "gastos_legales": gastos, "valor_estimado_batna": valor_estimado})
            self.lbl_res_litigio.text = res
        except ValueError:
            self.lbl_res_litigio.text = f"[color={ROJO_HEX}]Error: Verifica los valores numéricos.[/color]"

    # --- PESTAÑA COMERCIAL ---------------------------------------------
    def crear_vista_comercial(self):
        vista, self.lbl_res_comercial = self._formulario(
            "BATNA Comercial con Riesgo",
            [
                ("input_val_base", "Valor base sin riesgo ($)"),
                ("input_prob_riesgo", "Probabilidad de riesgo (0-100 %)"),
                ("input_prob_perder_r", "Prob. perder si ocurre riesgo (0-100 %)"),
                ("input_val_piso", "Valor si ocurre riesgo y pierdes ($)"),
                ("input_val_techo", "Valor si ocurre riesgo y ganas ($)"),
            ],
            "Calcular Valor Comercial",
            self.calcular_comercial,
            "Resultados...",
        )
        return vista

    def calcular_comercial(self, instance):
        try:
            v_base = float(self.input_val_base.text)
            p_riesgo = float(self.input_prob_riesgo.text) / 100.0
            p_perder_r = float(self.input_prob_perder_r.text) / 100.0
            v_piso = float(self.input_val_piso.text)
            v_techo = float(self.input_val_techo.text)

            p_ganar_r = 1.0 - p_perder_r
            v_conflicto = (p_perder_r * v_piso) + (p_ganar_r * v_techo)
            p_no_riesgo = 1.0 - p_riesgo
            v_final = (p_riesgo * v_conflicto) + (p_no_riesgo * v_base)

            res = f"[b][color={VIOLETA_HEX}]VALOR REAL BATNA COMERCIAL: ${v_final:,.2f}[/color][/b]"
            guardar_en_historial("Comercial Avanzado", {"valor_base": v_base, "probabilidad_riesgo": p_riesgo, "valor_estimado_final": v_final})
            self.lbl_res_comercial.text = res
        except ValueError:
            self.lbl_res_comercial.text = f"[color={ROJO_HEX}]Error: Verifica los datos introducidos.[/color]"

    # --- PESTAÑA HISTORIAL ---------------------------------------------
    def crear_vista_historial(self):
        tarjeta = Tarjeta(auto=False)
        tarjeta.add_widget(titulo("Historial"))

        btn_cargar = BotonCipher(text="Cargar / Actualizar Historial")
        btn_cargar.bind(on_release=self.mostrar_historial)
        tarjeta.add_widget(btn_cargar)

        self.lbl_historial = Texto(
            text="Presiona el botón para cargar registros.", font_size=sp(14)
        )
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(self.lbl_historial)
        tarjeta.add_widget(scroll)

        contenedor = BoxLayout(padding=[0, dp(4)])
        contenedor.add_widget(tarjeta)
        return contenedor

    def mostrar_historial(self, instance):
        if not os.path.exists(ARCHIVO_HISTORIAL):
            self.lbl_historial.text = "No hay registros guardados."
            return

        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not data:
                self.lbl_historial.text = "Historial vacío."
                return

            texto = ""
            for idx, item in enumerate(data, 1):
                texto += (
                    f"[b][color={VIOLETA_HEX}][{idx}][/color] "
                    f"{escape_markup(str(item['fecha']))} | "
                    f"{escape_markup(str(item['tipo']))}[/b]\n"
                )
                for k, v in item["resultado"].items():
                    texto += f"   • {escape_markup(str(k))}: {escape_markup(str(v))}\n"
                texto += "- - - - - - - - - - - - - - - - - - - -\n"
            self.lbl_historial.text = texto
        except Exception as e:
            self.lbl_historial.text = f"Error al leer historial: {escape_markup(str(e))}"

    # --- PESTAÑA AUTOR -------------------------------------------------
    def crear_vista_autor(self):
        caja = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[0, dp(4)],
        )
        caja.bind(minimum_height=caja.setter("height"))

        tarjeta = Tarjeta(spacing=dp(8))
        tarjeta.add_widget(titulo("Autoría", halign="center"))

        if os.path.exists(RUTA_LOGO):
            tarjeta.add_widget(
                Image(source=RUTA_LOGO, size_hint_y=None, height=dp(110))
            )

        tarjeta.add_widget(titulo(AUTOR, tam=20, halign="center"))
        tarjeta.add_widget(Texto(text=GIRO, halign="center", font_size=sp(16)))
        tarjeta.add_widget(
            Texto(text=f"Cédula profesional: [b]{CEDULA}[/b]", halign="center")
        )
        tarjeta.add_widget(
            Texto(text=f"WhatsApp: [b]{WHATSAPP}[/b]", halign="center")
        )
        tarjeta.add_widget(Texto(text=UBICACION, halign="center"))

        if os.path.exists(RUTA_QR):
            tarjeta.add_widget(
                Image(source=RUTA_QR, size_hint_y=None, height=dp(170))
            )

        tarjeta.add_widget(
            Texto(
                text=f"© {datetime.now().year} {AUTOR} · {EMPRESA}",
                halign="center",
                font_size=sp(12),
            )
        )
        caja.add_widget(tarjeta)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(caja)
        return scroll


class BatnaApp(App):
    title = f"BATNA · {EMPRESA}"

    def build(self):
        if os.path.exists(RUTA_LOGO):
            self.icon = RUTA_LOGO
        return CalculadoraPanel()


if __name__ == "__main__":
    BatnaApp().run()
