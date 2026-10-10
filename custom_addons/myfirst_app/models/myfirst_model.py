from odoo import models,fields

class MyFirstModel(models.Model):
    _name = 'myfirst.model'
    _description = 'My First Model'


    name=fields.Char(string="Name",required=True)
    long_text=fields.Char(string="Long Text")
    an_int=fields.Integer(string="An int Value")
    a_boolean=fields.Boolean(string="A Boolean Value")
    a_date=fields.Date(string="A Date Value")
    a_datetime=fields.Datetime(string="A Date & time Value")
    a_selection = fields.Selection(
        selection=[
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
        ],
        string='Selection Value',
    )
    a_html=fields.Html(string="Html Value"),
    a_binary=fields.Binary(string="Binary Value"),
    an_image=fields.Image(string="An Image Value"),
