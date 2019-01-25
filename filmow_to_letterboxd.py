import wx
import wx.lib.agw.hyperlink as hl
import webbrowser

from parser_filmow import Parser
from utils import delay

class Frame(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(Frame, self).__init__(*args, **kwargs)

    self.MyFrame = self

    self.is_running = False

    self.panel = wx.Panel(
      self,
      pos=(0, 0),
      size=(500,100),
      style=wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX | wx.SYSTEM_MENU
    )
    self.panel.SetBackgroundColour('#ffffff')
    self.SetTitle('Filmow to Letterboxd')
    self.SetMinSize((500, 300))
    self.SetMaxSize((500, 300))

    self.letterboxd_link = hl.HyperLinkCtrl(
      self.panel,
      -1,
      'letterboxd',
      URL='https://letterboxd.com/import/',
      pos=(420,240)
    )
    self.letterboxd_link.SetToolTip(wx.ToolTip('Clica só quando o programa tiver rodado e sua conta no Letterboxd tiver criada, beleza?'))

    self.coffee_link = hl.HyperLinkCtrl(
      self.panel,
      -1,
      'quer me agradecer?',
      URL='https://www.buymeacoffee.com/yanari',
      pos=(310,240)
    )
    self.coffee_link.SetToolTip(wx.ToolTip('Se tiver dado tudo certo cê pode me pagar um cafézinho, que tal?. Não é obrigatório, claro.'))

    wx.StaticText(self.panel, -1, 'Username no Filmow:', pos=(25, 54))
    self.username = wx.TextCtrl(self.panel,  size=(200, 25), pos=(150, 50))
    submit_button = wx.Button(self.panel, wx.ID_SAVE, 'Submit', pos=(360, 50))

    self.Bind(wx.EVT_BUTTON, self.Submit, submit_button)
    self.Bind(wx.EVT_CLOSE, self.OnClose)

    self.Show(True)


  def Submit(self, event):
    self.button = event.GetEventObject()
    self.button.Disable()

    self.text_control = wx.TextCtrl(
      self.panel,
      -1,
      '',
      pos=(50, 120),
      size=(400, 100),
      style=wx.TE_MULTILINE | wx.TE_CENTRE | wx.TE_READONLY 
      | wx.TE_NO_VSCROLL | wx.TE_AUTO_URL | wx.TE_RICH2 | wx.BORDER_NONE
    )
    self.Parse(self.MyFrame)


  @delay(1.0)
  def Parse(self, MyFrame):
    self.user = self.username.GetValue().lower().strip()
    if len(self.user) == 0:
      self.is_running = False
      self.text_control.ChangeValue('O campo não deve ficar em branco.')
      self.button.Enable()
      return
    else:
      try:
        msg = """Seus filmes estão sendo importados no plano de fundo :)\n\n
          Não feche a janela e aguarde um momento."""
        
        self.text_control.ChangeValue(msg)
        self.is_running = True
        self.parser = Parser(self.user)

      except Exception:
        self.text_control.ChangeValue('Usuário {} não encontrado. Tem certeza que digitou certo?'.format(self.user))
        self.button.Enable()
        self.is_running = False
        return
    
    self.ChangeMsg()
    
  
  @delay(1.0)
  def ChangeMsg(self):
    msg = """Pronto!\n\n Agora clica no link aqui embaixo pra ir pro Letterboxd, 
      SELECT A FILE e selecione o(s) arquivo(s) de extensão .csv 
      (tá tudo aqui nessa mesma pasta) criado(s) pelo programa."""

    self.text_control.ChangeValue(msg)
    self.Bind(wx.EVT_TEXT_URL, self.GoToLetterboxd, self.text_control)
    self.is_running = False


  def GoToLetterboxd(self, event):
    webbrowser.open('https://letterboxd.com/import/')


  def BuyMeACoffee(self, event):
    webbrowser.open('https://www.buymeacoffee.com/yanari')


  def OnClose(self, event):
    if self.is_running:
      confirm_exit = wx.MessageDialog(
        self,
        'Tem certeza que quer parar o programa?',
        'Sair',
        wx.YES_NO | wx.ICON_QUESTION
      )

      if confirm_exit.ShowModal() == wx.ID_YES:
        self.Destroy()
        wx.Window.Destroy(self)
      else:
        confirm_exit.Destroy()
    else:
      event.Skip()
    

if __name__ == '__main__':
  app = wx.App()
  Frame(None, size=(500, 300))
  app.MainLoop()