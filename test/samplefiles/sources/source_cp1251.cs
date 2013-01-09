using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.Net;
using Core;
using Core.Log;

namespace LJWatcher
{
	public partial class AuthForm : Form
	{
		CookieCollection _cookies = new CookieCollection ();

		public CookieCollection Cookies
		{
			get { return _cookies; }
		}

		public AuthForm ()
		{
			InitializeComponent ();

			savePassword.Checked = Config.Instance.SavePassword;

			if (Config.Instance.SavePassword)
			{
				usernameTextBox.Text = Config.Instance.Username;
				passwordTextBox.Text = DecryptPassword ();
			}
		}

		private static string DecryptPassword ()
		{
			string password = "";

			if (Config.Instance.Password.Length != 0)
			{
				SimpleAES aes = new SimpleAES ();
				password = aes.DecryptString (Config.Instance.Password);
			}
			return password;
		}

		private void loginButton_Click (object sender, EventArgs e)
		{
			LJServer server = new FlatLJServer ();
			try
			{
				_cookies = server.GetBaseCookie (usernameTextBox.Text, passwordTextBox.Text);
			}
			catch (WebException error)
			{
				MessageBox.Show ("Ошибка соединения с сервером.\n" + error.Message,
					"Ошибка",
					MessageBoxButtons.OK,
					MessageBoxIcon.Error);
				return;
			}

			if (_cookies.Count < 3)
			{
				MessageBox.Show ("Ошибка авторизации", 
					"Ошибка", 
					MessageBoxButtons.OK, 
					MessageBoxIcon.Error);
				return;
			}

			this.DialogResult = DialogResult.OK;
			this.Close ();
		}


		private void SaveParams ()
		{
			Config.Instance.SavePassword = savePassword.Checked;
			if (savePassword.Checked)
			{
				Config.Instance.Username = usernameTextBox.Text;
				Config.Instance.Password = EncryptPassword ();
			}
			else
			{
				Config.Instance.Username = "";
				Config.Instance.Password = "";
			}
		}


		private string EncryptPassword ()
		{
			string password = "";

			if (passwordTextBox.Text.Length != 0)
			{
				SimpleAES aes = new SimpleAES ();
				password = aes.EncryptToString (passwordTextBox.Text);
			}
			return password;
		}

		private void AuthForm_FormClosed (object sender, FormClosedEventArgs e)
		{
			SaveParams ();
		}
	}
}