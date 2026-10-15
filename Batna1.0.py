"""
=============================================================================
MÓDULO: CALCULADORA DE ESTRATEGIA DE NEGOCIACIÓN (ZOPA Y BATNA)
=============================================================================
Descripción:
Herramienta interactiva basada en los principios de negociación estratégica de 
George Siedel. Permite calcular y analizar:
  1. La Zona de Posible Acuerdo (ZOPA) entre compradores y vendedores.
  2. El valor esperado del BATNA en litigios o demandas judiciales (Árbol de Decisión).
  3. Análisis de BATNA comercial con incertidumbre y riesgo avanzado.
  4. Reglas clave de poder y tácticas de negociación.

Autor: Ing. Norberto Hdz.
Cédula Profesional: 15061201
=============================================================================
"""

import sys

def solicitar_dinero(mensaje):
    """Fuerza al usuario a introducir un número válido para dinero."""
    while True:
        entrada = input(mensaje).strip().replace("$", "").replace(",", "")
        try:
            return float(entrada)
        except ValueError:
            print("❌ Entrada inválida. Por favor, introduce solo números (ej: 4500 o 4500.50).")

def solicitar_porcentaje(mensaje):
    """Fuerza al usuario a introducir un porcentaje entre 0 y 100."""
    while True:
        entrada = input(mensaje).strip().replace("%", "")
        try:
            valor = float(entrada)
            if 0 <= valor <= 100:
                return valor / 100  # Lo convierte a decimal (ej: 85% -> 0.85)
            else:
                print("❌ El porcentaje debe estar entre 0 y 100.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, introduce un número (ej: 50 o 7.5).")

def menu_zopa():
    print("\n--- 🛒 MÓDULO: CÁLCULO DE LA ZOPA ---")
    reserva_vendedor = solicitar_dinero("Introduce el Precio de Reserva del VENDEDOR (Mínimo a aceptar): $")
    reserva_comprador = solicitar_dinero("Introduce el Precio de Reserva del COMPRADOR (Máximo a pagar): $")
    
    print("\n📊 --- RESULTADO DE LA ZOPA ---")
    if reserva_comprador >= reserva_vendedor:
        excedente = reserva_comprador - reserva_vendedor
        print(f"✅ ¡Existe una ZOPA viable!")
        print(f"   • Rango de acuerdo: Entre ${reserva_vendedor:,.2f} y ${reserva_comprador:,.2f}")
        print(f"   • Excedente total en juego: ${excedente:,.2f} (¡Esto es lo que vas a negociar para repartir!)")
    else:
        brecha = reserva_vendedor - reserva_comprador
        print(f"❌ NO EXISTE ZOPA. Las expectativas económicas no se cruzan.")
        print(f"   • Brecha económica: ${brecha:,.2f}")
        print(f"   👉 Consejo de George Siedel: Detén la negociación de inmediato y ejecuta tu BATNA.")

def menu_litigio():
    print("\n--- ⚖️ MÓDULO: BATNA EN RESOLUCIÓN DE DISPUTAS (LITIGIOS) ---")
    monto_disputa = solicitar_dinero("Monto total económico en disputa (lo que demandas o te demandan): $")
    prob_ganar = solicitar_porcentaje("¿Qué probabilidad tienes de ganar el juicio? (0 a 100): ")
    gastos_legales = solicitar_dinero("Gastos estimados de abogados, peritos y corte: $")
    
    prob_perder = 1.0 - prob_ganar
    neto_ganar = monto_disputa - gastos_legales
    neto_perder = -gastos_legales
    
    valor_estimado = (prob_ganar * neto_ganar) + (prob_perder * neto_perder)
    
    print("\n📊 --- RESULTADO DEL ÁRBOL DE DECISIÓN DE LITIGIO ---")
    print(f"   • Escenario Victoria ({prob_ganar*100:.1f}%): Te quedan netos ${neto_ganar:,.2f}")
    print(f"   • Escenario Derrota ({prob_perder*100:.1f}%): Pierdes/Pagas netos ${neto_perder:,.2f}")
    print(f"💰 VALOR ESTIMADO DE TU BATNA (Ir a juicio): ${valor_estimado:,.2f}")
    print(f"\n👉 REGLA DE DECISIÓN ESTRATÉGICA:")
    if valor_estimado > 0:
        print(f"   Si la contraparte te ofrece en la mesa de negociación un acuerdo DIRECTO mayor")
        print(f"   a ${valor_estimado:,.2f}, te conviene aceptar el acuerdo en lugar de ir a juicio.")
    else:
        print(f"   El valor de ir a juicio es negativo (${valor_estimado:,.2f}). Busca un acuerdo")
        print(f"   o retírate del conflicto lo antes posible para mitigar pérdidas.")

def menu_comercial_avanzado():
    print("\n--- 🏢 MÓDULO: BATNA COMERCIAL CON INCERTIDUMBRE (ÁRBOL DE DECISIÓN) ---")
    valor_base = solicitar_dinero("Valor base de tu alternativa comercial (si todo sale perfecto): $")
    prob_riesgo = solicitar_porcentaje("Probabilidad de que ocurra un evento de riesgo (ej: regulación, multa, bloqueo): ")
    prob_perder_riesgo = solicitar_porcentaje("Si el riesgo ocurre, ¿qué probabilidad hay de que lo pierdas/te sancionen?: ")
    valor_si_pierde_riesgo = solicitar_dinero("Valor del proyecto si el riesgo ocurre y te sancionan (Piso mínimo): $")
    valor_si_gana_riesgo = solicitar_dinero("Valor del proyecto si el riesgo ocurre pero sales absuelto/ganas: $")
    
    # Inducción hacia atrás
    prob_ganar_riesgo = 1.0 - prob_perder_riesgo
    valor_si_hay_conflicto = (prob_perder_riesgo * valor_si_pierde_riesgo) + (prob_ganar_riesgo * valor_si_gana_riesgo)
    
    prob_no_riesgo = 1.0 - prob_riesgo
    valor_estimado_final = (prob_riesgo * valor_si_hay_conflicto) + (prob_no_riesgo * valor_base)
    
    print("\n📊 --- RESULTADO DEL ANÁLISIS COMERCIAL AJUSTADO AL RIESGO ---")
    print(f"   • Valor esperado SI ocurre el evento de riesgo: ${valor_si_hay_conflicto:,.2f}")
    print(f"   • Valor esperado SI NO ocurre ningún riesgo: ${valor_base:,.2f}")
    print(f"💰 VALOR REAL DE TU BATNA COMERCIAL (Ajustado): ${valor_estimado_final:,.2f}")
    print(f"   👉 Consejo: Usa este valor (${valor_estimado_final:,.2f}) como tu punto de comparación real")
    print(f"      frente a la oferta que te están haciendo en la mesa actual.")

def mostrar_estrategias():
    print("\n=====================================================================")
    print("      💡 LAS 3 REGLAS DE PODER PARA EL BATNA (GEORGE SIEDEL)         ")
    print("=====================================================================")
    print("1. 🔍 INVESTIGA EL BATNA DE ELLOS: No te estanques en tus datos. Haz preguntas")
    print("   indirectas para descubrir cuál es la alternativa si ellos se levantan de la mesa.")
    print("2. 📉 DEBILITA SU BATNA: Haz que su alternativa parezca más costosa, lenta o")
    print("   arriesgada de lo que ellos creen (ej: recuérdales los tiempos de la corte).")
    print("3. 📈 MEJORA TU PROPIO BATNA: Nunca vayas a una negociación importante sin")
    print("   antes haber hablado o cotizado al menos con un tercero.")
    print("=====================================================================")

def ejecutor_calculadora():
    while True:
        print("\n=====================================================================")
        print("         CALCULADORA DE ESTRATEGIA DE NEGOCIACIÓN (SIEDEL)           ")
        print("=====================================================================")
        print("1) Calcular ZOPA (Zona de Posible Acuerdo)")
        print("2) Calcular BATNA para Litigios / Demandas judiciales")
        print("3) Calcular BATNA Comercial con Riesgo Avanzado (Árbol de Decisión)")
        print("4) Ver Estrategias de Poder sobre el BATNA")
        print("5) Salir")
        print("=====================================================================")
        
        opcion = input("Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            menu_zopa()
        elif opcion == "2":
            menu_litigio()
        elif opcion == "3":
            menu_comercial_avanzado()
        elif opcion == "4":
            mostrar_estrategias()
        elif opcion == "5":
            print("\n👋 ¡Éxito en tus negociaciones! Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida. Por favor, selecciona un número del 1 al 5.")

# Iniciar la calculadora interactiva
if __name__ == "__main__":
    ejecutor_calculadora()
