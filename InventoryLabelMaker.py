# coding: utf-8

from fpdf import FPDF
import qrcode

class InventoryLabelMaker:
    def __init__(self):
        self.LabelWidth = 89
        self.LabelHeight = 36
        self.Font = "Arial"
        self.TitleFontsize = 12
        self.InvNrFontsize = 10
        self.UrlFontsize = 8
        self.Prefix = "g"
        self.QRcodeExt = "png"
        self.PdfExt = "pdf"
        self.ShortBaseUrl = "http://hshb.de"

    def MakeLabel(self, number, title):
        self.InvNumber = self.Prefix + format(int(number), "04")
        self.ShortUrl = "/".join([self.ShortBaseUrl, self.InvNumber])
        self.QRcodeFileName = ".".join([self.InvNumber, self.QRcodeExt])
        self.PdfFileName = ".".join([self.InvNumber, self.PdfExt])

        self.Label = FPDF('L', 'mm', (self.LabelHeight, self.LabelWidth))
        self.Label.set_auto_page_break(False)
        self.Label.add_page()
        self.Label.set_font(self.Font, '', self.TitleFontsize)
        self.Label.set_xy(5, 6)
        self.Label.multi_cell(55,5,title)

        self.Label.set_font(self.Font, 'U', self.InvNrFontsize)
        self.Label.set_xy(5, 27)
        len_inv = self.Label.get_string_width('Inventar-Nr: ')
        self.Label.cell(len_inv,0,'Inventar-Nr:')
        self.Label.set_font(self.Font, '', self.InvNrFontsize)
        self.Label.cell(0,0,self.InvNumber)

        self.QRcode = qrcode.make(self.ShortUrl)
        self.QRcode.save(self.QRcodeFileName)

        self.Label.image(self.QRcodeFileName, x = 61, y = 2, w = 25)

        self.Label.set_font(self.Font, '', self.UrlFontsize)
        self.Label.set_xy(63, 27)
        self.Label.cell(0,0,self.ShortUrl[7:])

        self.Label.output(self.PdfFileName)

