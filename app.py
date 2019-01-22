import wx
from filmow_to_letterboxd import Parser

class Window(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(Window, self).__init__(*args, **kwargs)

    self.basicGUI()
  
  def basicGUI(self):
    panel = wx.Panel(self)

    wx.StaticText(panel, -1, 'Username no Filmow:', pos=(25, 54))

    self.username = wx.TextCtrl(panel,  size=(200, 25), pos=(150, 50))

    submit_button = wx.Button(panel, wx.ID_SAVE, 'Submit', pos=(360, 50))

    self.Bind(wx.EVT_BUTTON, self.Submit, submit_button)
    

    self.SetTitle('Filmow to Letterboxd')
    self.Show(True)
  
  def Quit(self, e):
    self.Close()

  def Submit(self, e):
    Parser(self.username.GetValue())

app = wx.App()
Window(None, size=(500, 300))
app.MainLoop()