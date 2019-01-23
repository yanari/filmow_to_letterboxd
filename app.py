import wx
import wx.lib.scrolledpanel
from filmow_to_letterboxd import Parser
from utils import delay

class Frame(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(Frame, self).__init__(*args, **kwargs)

    self.user_panel = wx.Panel(
      self,
      pos=(0, 0),
      size=(500,100),
      style=wx.DEFAULT_FRAME_STYLE
    )
    self.user_panel.SetBackgroundColour('#ffffff')

    wx.StaticText(self.user_panel, -1, 'Username no Filmow:', pos=(25, 54))
    self.username = wx.TextCtrl(self.user_panel,  size=(200, 25), pos=(150, 50))
    submit_button = wx.Button(self.user_panel, wx.ID_SAVE, 'Submit', pos=(360, 50))


    self.Bind(wx.EVT_BUTTON, self.Submit, submit_button)

    self.SetTitle('Filmow to Letterboxd')
    self.Show(True)
  
  def Quit(self, event):
    self.Close()

  def Submit(self, event):
    button = event.GetEventObject()
    button.Disable()

    msg = 'Seus filmes estão sendo importados no plano de fundo :)\nNão feche a janela e aguarde um momento.'
    self.text_control = wx.TextCtrl(
      self.user_panel,
      -1,
      msg,
      pos=(50, 120),
      size=(400, 50),
      style=wx.TE_MULTILINE | wx.TE_CENTRE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.TE_AUTO_URL | wx.TE_RICH
    )

    self.Parse()
  
  def GoToLetterboxd(self, event):
    pass

    
  @delay(3.0)
  def Parse(self):
    Parser(self.username.GetValue())
    self.ChangeMsg()
    
  
  @delay(1.0)
  def ChangeMsg(self):
    self.text_control.ChangeValue('Pronto!\n Agora vá para https://letterboxd.com/import/, clique em SELECT A FILE e selecione o(s) arquivo(s) de extensão .csv criado(s) pelo programa.')
    self.Bind(wx.EVT_TEXT_URL, self.GoToLetterboxd, self.text_control)



if __name__ == '__main__':
  app = wx.App()
  Frame(None, size=(500, 300))
  app.MainLoop()