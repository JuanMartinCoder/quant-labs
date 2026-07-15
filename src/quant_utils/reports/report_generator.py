# src/quants_utils/reports/report_generator.py

import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .styles import InstitutionalStyle

class ReportGenerator:
    def __init__(self, output_path: str):
        # Configuración de márgenes institucionales (A4)
        self.doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        self.styles = getSampleStyleSheet()
        self.elements = []
        self._custom_styles()

    def _custom_styles(self):
        """Agrega tipografías personalizadas alineadas al diseño corporativo."""
        self.styles.add(ParagraphStyle('MainTitle', fontName=InstitutionalStyle.FONT_BOLD, fontSize=24, leading=28, textColor=colors.HexColor(InstitutionalStyle.PRIMARY_BLUE)))
        self.styles.add(ParagraphStyle('SubTitle', fontName=InstitutionalStyle.FONT, fontSize=9, leading=12, textColor=colors.HexColor("#7f8c8d")))
        self.styles.add(ParagraphStyle('SectionHeading', fontName=InstitutionalStyle.FONT_BOLD, fontSize=14, leading=18, textColor=colors.HexColor(InstitutionalStyle.PRIMARY_BLUE)))
        self.styles.add(ParagraphStyle('TableHeader', fontName=InstitutionalStyle.FONT_BOLD, fontSize=9, leading=11, textColor=colors.white, alignment=1))
        self.styles.add(ParagraphStyle('TableCell', fontName=InstitutionalStyle.FONT, fontSize=9, leading=11, alignment=1))
        self.styles.add(ParagraphStyle('Disclaimer', fontName=InstitutionalStyle.FONT, fontSize=7, leading=9, textColor=colors.HexColor("#95a5a6")))
        self.styles.add(ParagraphStyle(name='TextoCorporativo', fontName='Helvetica',  fontSize=10, leading=14, textColor=colors.HexColor('#2D3748')))
    def construir_reporte(self, metadata: dict, 
                          df_kpis: list, 
                          df_friccion: list, 
                          path_chart_line: str, 
                          path_chart_pie: str,
                          tabla_rendimientos_mensuales: list = None,
                          tabla_asset_allocation: list = None,
                          tabla_profit_neto: list = None,
                          ticker_benchmark: str = None,
                          tabla_mercado_data: list = None):
        """Ensambla secuencialmente la estructura visual completa del PDF."""
        
        # === ENCABEZADO PRINCIPAL ===
        self.elements.append(Paragraph("REPORTE DE ANÁLISIS OPERATIVO DE ESTRATEGIAS", self.styles['MainTitle']))
        self.elements.append(Spacer(1, 6))
        
        meta_text = f"Analista Principal: {metadata.get('analista')} | Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | Estructura Arbitrada: {metadata.get('label_broker')}"
        self.elements.append(Paragraph(meta_text, self.styles['SubTitle']))
        self.elements.append(Spacer(1, 8))
        
        # Línea divisoria verde corporativa
        self.elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor(InstitutionalStyle.SUCCESS_COLOR), spaceAfter=15))

        self.elements.append(Paragraph("CONTEXTO DEL ANÁLISIS DE RENDIMIENTO", self.styles['SectionHeading']))
        self.elements.append(Spacer(1, 8))

        # 2. Bloque descriptivo institucional (Tomado del diccionario 'metadata' del Notebook)
        descripcion_texto = metadata.get("descripcion_metodologica", "Análisis cuantitativo de portafolio.")
        self.elements.append(Paragraph(descripcion_texto, self.styles['TextoCorporativo'])) # Asegurate de usar el estilo de texto plano de tu clase
        self.elements.append(Spacer(1, 12))

        # 3. Cuadro resumido de parámetros temporales y monetarios
        tabla_metadata_datos = [
            [Paragraph("<b>Monto Inicial de Prueba:</b>", self.styles['TextoCorporativo']), Paragraph(metadata.get("capital_inicial_prueba", "-"), self.styles['TextoCorporativo'])],
            [Paragraph("<b>Fase Entrenamiento (IS):</b>", self.styles['TextoCorporativo']), Paragraph(metadata.get("fase_entrenamiento_is", "-"), self.styles['TextoCorporativo'])],
            [Paragraph("<b>Fase Validación (OOS):</b>", self.styles['TextoCorporativo']), Paragraph(metadata.get("fase_validacion_oos", "-"), self.styles['TextoCorporativo'])],
        ]

        # Construimos una tablita limpia sin bordes pesados para que parezca un bloque de datos del header
        t_meta = Table(tabla_metadata_datos, colWidths=[150, 300], hAlign='CENTER')
        t_meta.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2D3748')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F7FAFC')), # Fondo grisáceo muy sutil
        ]))

        self.elements.append(t_meta)
        self.elements.append(Spacer(1, 25))


        # === SECCIÓN 1: KPIs DE PERFORMANCE ===
        self.elements.append(Paragraph("1. ATRIBUCIÓN DE PERFORMANCE Y EFICIENCIA (KPIS)", self.styles['SectionHeading']))
        self.elements.append(Spacer(1, 8))
        
        # Renderizado de Tabla de KPIs con formateo condicional de colores (Rojo/Verde)
        kpi_table_data = [[Paragraph(col, self.styles['TableHeader']) for col in ["ESTRATEGIA", "RETORNO", "VOLATILIDAD", "SHARPE", "SORTINO", "MAX DD", "CALMAR","ALPHA (α) ANUAL"]]]
        
        for row in df_kpis:
            # Lógica para colorear condicionalmente MaxDD (Rojo) y Calmar (Verde)
            style_dd = ParagraphStyle('dd', parent=self.styles['TableCell'], textColor=colors.HexColor(InstitutionalStyle.DANGER_COLOR), fontName=InstitutionalStyle.FONT_BOLD)
            style_calmar = ParagraphStyle('cl', parent=self.styles['TableCell'], textColor=colors.HexColor(InstitutionalStyle.SUCCESS_COLOR), fontName=InstitutionalStyle.FONT_BOLD)
            
            # Lógica para colorear condicionalmente Alpha (Rojo) y Calmar (Verde)
            if row[7] > 0.00:
                style_alpha = ParagraphStyle('alpha', parent=self.styles['TableCell'], textColor=colors.HexColor(InstitutionalStyle.SUCCESS_COLOR), fontName=InstitutionalStyle.FONT_BOLD)
            elif row[7] < 0.00:
                style_alpha = ParagraphStyle('alpha', parent=self.styles['TableCell'], textColor=colors.HexColor(InstitutionalStyle.DANGER_COLOR), fontName=InstitutionalStyle.FONT_BOLD)
            else:
                style_alpha = self.styles['TableCell']

            alpha = f"{row[7]:.2%}"
            if row[7] > 0.00:
                alpha = f"+{alpha}"

            kpi_table_data.append([
                Paragraph(str(row[0]), self.styles['TableCell']),
                Paragraph(f"{row[1]:.2%}", self.styles['TableCell']),
                Paragraph(f"{row[2]:.2%}", self.styles['TableCell']),
                Paragraph(f"{row[3]:.2f}", self.styles['TableCell']),
                Paragraph(f"{row[4]:.2f}", self.styles['TableCell']),
                Paragraph(f"{row[5]:.2%}", style_dd),
                Paragraph(f"{row[6]:.2f}", style_calmar),
                Paragraph(alpha, style_alpha)
            ])
            
        t_kpi = Table(kpi_table_data, colWidths=[130, 65, 75, 55, 55, 65, 55])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(InstitutionalStyle.PRIMARY_BLUE)),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(InstitutionalStyle.GRID_COLOR)),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        self.elements.append(t_kpi)
        self.elements.append(Spacer(1, 15))

        self.elements.append(Paragraph(f"ATRIBUCIÓN DE RIESGO SISTEMÁTICO VS BENCHMARK ({ticker_benchmark})", self.styles['SectionHeading']))
        self.elements.append(Spacer(1, 8))

        
        # Texto aclaratorio institucional
        aclaracion_riesgo = (
            "El siguiente cuadro detalla el riesgo sistemático de mercado de cada estrategia. "
            "La métrica de riesgo sistemático se calcula como el retorno esperado de un portafolio "
            "en el mercado de referencia, considerando el riesgo de pérdidas de capital."
        )
        self.elements.append(Paragraph(aclaracion_riesgo, self.styles['TextoCorporativo']))

        t_mercado = Table(tabla_mercado_data, hAlign='CENTER', colWidths=[140, 95, 105, 170])
        t_mercado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(InstitutionalStyle.PRIMARY_BLUE)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(InstitutionalStyle.GRID_COLOR)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ]))
        self.elements.append(t_mercado)
        self.elements.append(Spacer(1, 10))

        # === SECCIÓN 2: AUDITORÍA DE FRICCIÓN (TURNOVER) ===
        self.elements.append(Paragraph("2. AUDITORÍA DE FRICCIÓN Y COSTOS OPERATIVOS (TURNOVER)", self.styles['SectionHeading']))
        self.elements.append(Spacer(1, 8))
        
        friccion_table_data = [[
            Paragraph("MÉTRICA DE FRICCIÓN FINANCIERA", self.styles['TableHeader']),
            Paragraph("VALOR REGISTRADO", self.styles['TableHeader']),
            Paragraph("IMPACTO RELATIVO EN CARTERA", self.styles['TableHeader'])
        ]]
        
        for name, value, impact, is_danger in df_friccion:
            cell_style = self.styles['TableCell']
            if is_danger:
                cell_style = ParagraphStyle('danger_f', parent=self.styles['TableCell'], textColor=colors.HexColor(InstitutionalStyle.DANGER_COLOR))
            
            friccion_table_data.append([
                Paragraph(name, self.styles['TableCell']),
                Paragraph(value, cell_style),
                Paragraph(impact, cell_style)
            ])
            
        t_fricc = Table(friccion_table_data, colWidths=[210, 90, 220])
        t_fricc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(InstitutionalStyle.PRIMARY_BLUE)),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor(InstitutionalStyle.GRID_COLOR)),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f9fa")]),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#fadbd8")), # Fricción Total en rojo suave
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        self.elements.append(t_fricc)
        self.elements.append(Spacer(1, 15))

        # === SECCIÓN 3: VISUALIZACIÓN GRÁFICA ===
        self.elements.append(Paragraph("3. VISUALIZACIÓN GRÁFICA Y DISTRIBUCIÓN DE ACTIVOS", self.styles['SectionHeading']))
        self.elements.append(Spacer(1, 8))
        
        # Encapsulamos las dos imágenes lado a lado usando una tabla invisible
        img_line = Image(path_chart_line, width=280, height=140)
        img_pie = Image(path_chart_pie, width=220, height=140)
        
        t_charts = Table([[img_line, img_pie]], colWidths=[290, 230])
        t_charts.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        self.elements.append(t_charts)
        self.elements.append(Spacer(1, 15))

        # ==============================================================================
        # INYECCIÓN DEL CUADRO DE PROFIT NETO FINAL
        # ==============================================================================
        if tabla_profit_neto is not None:
            self.elements.append(Paragraph("RESUMEN DE CAPITAL Y PROFIT NETO FINAL (OOS)", self.styles['SectionHeading']))
            self.elements.append(Spacer(1, 4))
            
            # Texto aclaratorio institucional
            aclaracion_profit = (
                "El siguiente cuadro detalla el patrimonio neto final y la ganancia líquida absoluta "
                "obtenida por cada estrategia al cierre del período de validación, habiendo deducido "
                "el 100% de los costos operativos, aranceles de intermediación e IVA devengados por el broker."
            )
            self.elements.append(Paragraph(aclaracion_profit, self.styles['TextoCorporativo']))
            self.elements.append(Spacer(1, 10))
            
            # Maquetación de la tabla con ReportLab
            t_profit = Table(tabla_profit_neto, hAlign='LEFT', colWidths=[160, 100, 150, 100])
            t_profit.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F2942')), # Azul marino profundo institucional
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'), # Alineamos los nombres a la izquierda
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EDF2F7')), # Fondo gris azulado muy limpio
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('TEXTCOLOR', (2, 1), (2, -1), colors.HexColor('#2F855A')), # Resaltamos el Profit ganado en verde oscuro
                ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
            ]))
            
            self.elements.append(t_profit)
            self.elements.append(Spacer(1, 20))

        


        # Inyección de la Tabla de Rendimientos Mensuales
        if tabla_rendimientos_mensuales is not None:
            self.elements.append(Paragraph("3. RENDIMIENTO MENSUAL DETALLADO (OOS)", self.styles['SectionHeading']))
            self.elements.append(Spacer(1, 10))
            
            # Convertimos la lista de listas en una tabla de ReportLab
            t_mensual = Table(tabla_rendimientos_mensuales, hAlign='CENTER')
            t_mensual.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')), # Encabezado institucional
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F7FAFC')), # Fondo suave para datos
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
            ]))
            self.elements.append(t_mensual)
            self.elements.append(Spacer(1, 20))

        # Inyección de la Tabla de Asset Allocation Mensual
        if tabla_asset_allocation is not None:
            self.elements.append(Paragraph("4. EVOLUCIÓN MENSUAL DEL ASSET ALLOCATION", self.styles['SectionHeading']))
            self.elements.append(Spacer(1, 10))
            
            t_allocation = Table(tabla_asset_allocation, hAlign='CENTER')
            t_allocation.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2D3748')), # Encabezado gris oscuro
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ]))
            self.elements.append(t_allocation)
            self.elements.append(Spacer(1, 20))
        
        # === DISCLAIMER LEGAL REGULATORIO ===
        disclaimer_text = ("Disclaimer Legal / Advertencia de Riesgo: Los rendimientos históricos expuestos en este "
                           "informe son simulaciones computacionales (backtesting out-of-sample) y no garantizan ni aseguran "
                           "ganancias o comportamientos idénticos en el futuro. Las inversiones en instrumentos de renta variable, "
                           "CEDEARs y derivados conllevan riesgos sustanciales de pérdida de capital. Este documento se distribuye "
                           "exclusivamente con fines académicos y de investigación cuantitativa, y no constituye de ninguna forma una oferta "
                           "explícita de venta, recomendación de inversión o asesoramiento financiero bajo las regulaciones de la CNV.")
        self.elements.append(Paragraph(disclaimer_text, self.styles['Disclaimer']))

    def generar(self):
        self.doc.build(self.elements)