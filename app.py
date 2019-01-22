import wx
from filmow_to_letterboxd import Parser

class WindowClass(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(WindowClass, self).__init__(*args, **kwargs)

    self.basicGUI()
  
  def basicGUI(self):
    panel = wx.Panel(self)

    menu_bar = wx.MenuBar()

    file_button = wx.Menu()
    edit_button = wx.Menu()

    exit_item = file_button.Append(wx.ID_EXIT, 'Exit')

    menu_bar.Append(file_button, 'File')
    menu_bar.Append(edit_button, 'Edit')

    self.text = wx.TextCtrl(panel,  size=(200, 25), pos=(50, 50))

    submit_button = wx.Button(panel, wx.ID_SAVE, 'Submit', pos=(260, 50))

    self.SetMenuBar(menu_bar)
    self.Bind(wx.EVT_MENU, self.Quit, exit_item)

    self.Bind(wx.EVT_BUTTON, self.Submit, submit_button)
    

    self.SetTitle('Filmow to Letterboxd')
    self.Show(True)
  
  def Quit(self, e):
    self.Close()

  def Submit(self, e):
    print(self.text.GetValue())
    Parser(self.text.GetValue())

app = wx.App()
WindowClass(None)
app.MainLoop()