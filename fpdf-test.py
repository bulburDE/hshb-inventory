# coding: utf-8

from fpdf import FPDF
import qrcode

pdf = FPDF('L', 'mm', (36, 89))
pdf.set_auto_page_break(False)
pdf.add_page()
pdf.set_font('Arial', '', 12)
pdf.set_xy(5, 6)
pdf.cell(0,0,'Some awesome Device')

pdf.set_font('Arial', 'U', 10)
pdf.set_xy(5, 27)
len_inv = pdf.get_string_width('Inventar-Nr: ')
pdf.cell(len_inv,0,'Inventar-Nr:')
pdf.set_font('Arial', '', 10)
pdf.cell(0,0,'g0001')

img = qrcode.make('http://hshb.de/g0001')
img.save('g0001.png')

pdf.image('g0001.png', x = 61, y = 2, w = 25)

pdf.set_font('Arial', '', 8)
pdf.set_xy(63, 27)
pdf.cell(0,0,'hshb.de/g0001')

pdf.output('test.pdf')
