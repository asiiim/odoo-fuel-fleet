# -*- coding: utf-8 -*-

from odoo import models, fields, _
import datetime
from datetime import datetime, timedelta, date
import pytz


class StockReportXls(models.AbstractModel):
    _name = 'report.generic_stock_report.stock_excel_report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Stock Report by Product Category')
        
        self.print_header(data, workbook, sheet)
        # self.print_stock_report(data, workbook, sheet)

        # Manual adjustment of the columns width
        
        sheet.set_column(0, 5, 10)
        sheet.set_column(6, 8, 15)

        # sheet.set_column(1, 1, 40)
        # sheet.set_column(3, 5, 15)
        # sheet.set_column(7, 10, 15)
        # sheet.set_column(11, 11, 20)


    def check_product_moves(self, product, dt):
        '''
            - Check the product moves with domain such that
                - date is less than or equal to the param date
                - if no records than return False else return True
        '''
        product_moves = self.env['stock.move.line'].search([
            ('date', '<=', dt),
            ('product_id', '=', product.id)
        ])
        if product_moves:
            return True
        else:
            return False


    def print_header(self, data, workbook, sheet):
        format_header = workbook.add_format({
            'font_name': 'Arial',
            'font_size': 12, 
            'align': 'center', 
            'bold': True,
            'bg_color': 'blue', 
            'font_color': 'white',
            'border':1,
            'border_color': '#000000'})
        format_header_no_bg = workbook.add_format({
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
             'bold': True
        })
        format_header_title = workbook.add_format({
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
            'bold': True
        })
        
        company = self.env['res.company'].search(
            [('id','=',data['form']['company_id'])])
        # user = self.env.user.name
        # tz = pytz.timezone(self.env.user.tz) \
            # if self.env.user.tz else pytz.timezone("Asia/Kathmandu")
        # time = pytz.utc.localize(datetime.now()).astimezone(tz)
        
        
        # sheet.merge_range('B1:I1', 'Generated On : ' \
        #     + str(time.strftime("%d/%m/%Y, %I:%M:%S %p")) \
        #         + "\t \t \t By:  " + str(user), format_header_no_bg)
        
        sheet.merge_range('B2:I2', company.name, format_header_title)
        sheet.merge_range('B4:I4', 'Location: '+ str(
            data['location']), format_header_no_bg)
        sheet.merge_range('B5:I5', 
            'Stock Report of %s' % data['product_name'], format_header_title)


        sheet.write('A6', 'From', format_header_no_bg)
        sheet.write('A7',  data['form']['start_date'], format_header_no_bg)
        sheet.write('I6', 'To', format_header_no_bg)
        sheet.write('I7',  data['form']['end_date'], format_header_no_bg)
        
        sheet.write('A9', 'Date', format_header)
        sheet.write('B9', 'Beginning', format_header)
        sheet.write('C9', 'Purchases', format_header)
        sheet.write('D9', 'Transfers', format_header)
        sheet.write('E9', 'Sales', format_header)

        sheet.write('F8', 'Calculated', format_header)
        sheet.write('F9', 'Ending', format_header)

        sheet.write('G8', 'Physical', format_header)
        sheet.write('G9', 'Tank Reading', format_header)
        
        sheet.write('H9', 'Adjustment', format_header)
        
        sheet.write('I8', 'Cumulative', format_header)
        sheet.write('I9', 'Adjustment', format_header)
        

    # def get_records(self,data, location=None,product_id=None):
    #     '''
    #     @param start_date: start date
    #     @param end_date: end date
    #     @param location_id: location ID
    #     @param product_id: Product IDs
    #     @returns: recordset
    #     '''
    #     domains = []
    #     domains += [
    #         ('date', '>=', data['form']['start_date']),
    #         ('date', '<=', data['form']['end_date']),
    #         ('state', '=', 'done'),
    #         ('product_id.id', '=', product_id),
    #         '|',
    #         ('location_id.id', '=', location),
    #         ('location_dest_id.id', '=', location)
    #     ]
    #     records = self.env['stock.move.line'].search(domains, order='date asc')
    #     product_id = self.env['product.product'].search([
    #         ('id','=',product_id),('type','=','product')])
    #     location_name = self.env['stock.location'].search([('id','=',location)]).display_name
    #     opening_date = datetime.strptime(
    #         data['form']['start_date'], "%Y-%m-%d").date() + timedelta(days=-1)
    #     closing_date = datetime.strptime(
    #         data['form']['end_date'], "%Y-%m-%d").date()
    #     opening = product_id.with_context({'to_date': str(opening_date),'location': location}).qty_available

    #     if opening < 0 and not self.check_product_moves(product_id, opening_date):
    #         opening = 0.0

    #     opening_value = product_id.with_context({'to_date': str(opening_date),'location': location}).value_svl
    #     closing = product_id.with_context({'to_date': str(closing_date),'location': location}).qty_available
    #     closing_value = product_id.with_context({'to_date': str(closing_date),'location': location}).value_svl
    #     total_in = 0
    #     total_in_value =0
    #     for record in (records.filtered(lambda r: r.location_dest_id.id == location)):
    #         total_in += record.product_uom_id._compute_quantity(record.qty_done, record.product_id.uom_id)
    #         total_in_value += record.qty_done
    #     total_out = 0 
    #     total_out_value = 0
    #     for record in (records.filtered(lambda r: r.location_id.id == location)):
    #         total_out += record.product_uom_id._compute_quantity(record.qty_done, record.product_id.uom_id)
    #         total_out_value += record.qty_done
    #     summary = {
    #         'barcode': product_id.barcode,
    #         'product' : product_id,
    #         'product_name': product_id.name,
    #         'product_uom' : product_id.uom_id.name,
    #         'mrp': product_id.lst_price,
    #         'opening': opening,
    #         'closing': closing,
    #         'total_in' :total_in,
    #         'total_out' : total_out,
    #     }
    #     return summary
    
    
    # def print_stock_report(self, data, workbook, sheet):

    #     format_total_string = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 
    #         'align': 'center', 'bold': True,
    #         'bg_color': 'blue', 'font_color': 'white', 'border':1, 'border_color': '#000000'})
    #     format_total_numeric = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 'align': 'right', 
    #         'bold': True, 'num_format': '#,##0.00', 
    #         'bg_color': 'blue', 'font_color': 'white', 'border':1, 'border_color': '#000000'})
    #     format_string_left = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 
    #         'align': 'left','bold': False, 'border':1, 'border_color': '#000000'})
    #     format_string_right = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 
    #         'align': 'right','bold': False, 'border':1, 'border_color': '#000000'})
    #     format_string_center = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 
    #         'align': 'center','bold': False, 'border':1, 'border_color': '#000000'})
    #     format_numeric_right = workbook.add_format({
    #         'font_name': 'Arial','font_size': 12, 
    #         'align': 'right', 'num_format': '#,##0.00',
    #         'bold': False, 'border':1, 'border_color': '#000000'})
        
    #     location = data['form']['location_id']
    #     product = data['form']['product_id']

    #     if not product:
    #         categ = data['product_category']
    #         products = self.env['product.product'].search(
    #             ['|', ('categ_id', '=?', categ), ('categ_id', 'child_of', categ)]).ids

    #     row = 8

    #     total_invoice_cost = total_import_cost = total_landed_cost = total_mrp\
    #         = total_opening = total_in = total_out = total_closing\
    #             = total_stock_valuation = 0.0

    #     for product in products:

    #         landed_cost = self.get_landed_cost(product, data)
    #         invoice_cost = round(self.get_invoice_cost(product, data), 2)

    #         summary = self.get_records(data, location=location, product_id=product)
            
    #         sheet.write(row, 0, summary['barcode'], format_string_center)
    #         sheet.write(row, 1, summary['product_name'], format_string_left)
    #         sheet.write(row, 2, summary['product_uom'], format_string_center)
    #         sheet.write(row, 3, invoice_cost, format_numeric_right)
    #         sheet.write(row, 4, landed_cost, format_numeric_right)
    #         sheet.write(row, 5, invoice_cost+landed_cost, format_numeric_right)
    #         sheet.write(row, 6, summary['mrp'], format_numeric_right)
    #         sheet.write(row, 7, summary['opening'], format_numeric_right)
    #         sheet.write(row, 8, summary['total_in'], format_numeric_right)
    #         sheet.write(row, 9, summary['total_out'], format_numeric_right)
    #         sheet.write(row, 10, summary['closing'], format_numeric_right)
    #         sheet.write(row, 11, 
    #             ((invoice_cost+landed_cost)*summary['closing']), 
    #             format_numeric_right)

    #         total_invoice_cost += invoice_cost
    #         total_import_cost += landed_cost
    #         total_landed_cost += (invoice_cost + landed_cost)
    #         total_mrp += summary['mrp']
    #         total_opening += summary['opening']
    #         total_in += summary['total_in']
    #         total_out += summary['total_out']
    #         total_closing += summary['closing']
    #         total_stock_valuation += (((invoice_cost+landed_cost)*summary['closing']))
            
    #         row += 1
    #     row += 1

    #     # Total amount
    #     sheet.merge_range(
    #         'A%s:C%s' % (str(row), str(row)), 
    #         'Total', 
    #         format_total_string
    #     )
    #     row -= 1
    #     sheet.write(row, 3, total_invoice_cost, format_total_numeric)
    #     sheet.write(row, 4, total_import_cost, format_total_numeric)
    #     sheet.write(row, 5, total_landed_cost, format_total_numeric)
    #     sheet.write(row, 6, total_mrp, format_total_numeric)
    #     sheet.write(row, 7, total_opening, format_total_numeric)
    #     sheet.write(row, 8, total_in, format_total_numeric)
    #     sheet.write(row, 9, total_out, format_total_numeric)
    #     sheet.write(row, 10, total_closing, format_total_numeric)
    #     sheet.write(row, 11, total_stock_valuation, format_total_numeric)

