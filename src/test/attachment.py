#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from core.attachment import Attachment
from utils import removeWiki
from core.tree import WikiDocument
from pages.text.textpage import TextPageFactory
from core.application import Application



class AttachmentTest (unittest.TestCase):
	def setUp (self):
		# Количество срабатываний особытий при обновлении страницы
		self.pageUpdateCount = 0
		self.pageUpdateSender = None

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		self.page = self.rootwiki[u"Страница 1"]

		filesPath = u"../test/samplefiles/"
		self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
		self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]


	def tearDown (self):
		removeWiki (self.path)


	def onPageUpdate (self, sender):
		self.pageUpdateCount += 1
		self.pageUpdateSender = sender


	def testAttachPath1 (self):
		attach = Attachment (self.page)
		self.assertEqual (attach.getAttachPath(), os.path.join (self.page.path, Attachment.attachDir))


	def testAttachPath2 (self):
		attach = Attachment (self.page)

		# Получить путь до прикрепленных файлов, не создавая ее
		path = attach.getAttachPath()
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertFalse (os.path.exists (path))
	

	def testAttachPath3 (self):
		attach = Attachment (self.page)

		# Получить путь до прикрепленных файлов, не создавая ее
		path = attach.getAttachPath(create=False)
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertFalse (os.path.exists (path))


	def testAttachPath4 (self):
		attach = Attachment (self.page)

		# Получить путь до прикрепленных файлов, создав ее
		path = attach.getAttachPath(create=True)
		# Вложенных файлов еще нет, поэтому нет и папки
		self.assertTrue (os.path.exists (path))


	def testEvent (self):
		self.pageUpdateCount = 0

		Application.onPageUpdate += self.onPageUpdate

		attach = Attachment (self.page)

		# Прикрепим к двум страницам файлы
		attach.attach (self.fullFilesPath [: 2])
		
		self.assertEqual (self.pageUpdateCount, 1)
		self.assertEqual (self.pageUpdateSender, self.page)

		attach.attach (self.fullFilesPath [2 :])
		
		self.assertEqual (self.pageUpdateCount, 2)
		self.assertEqual (self.pageUpdateSender, self.page)

		Application.onPageUpdate -= self.onPageUpdate


	def testAttach1 (self):
		attach = Attachment (self.page)
		attach.attach (self.fullFilesPath)

		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath))

		attachBasenames = [os.path.basename (path) for path in attach.attachmentFull]

		for path in self.fullFilesPath:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)

		for path in attach.attachmentFull:
			self.assertTrue (os.path.exists (path))


	def testAttach2 (self):
		attach = Attachment (self.page)
		attach2 = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		self.assertTrue (attach != attach2)
		self.assertEqual (len (attach2.attachmentFull), len (self.fullFilesPath))

		attachBasenames = [os.path.basename (path) for path in attach2.attachmentFull]

		for path in self.fullFilesPath:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)


	def testAttach3 (self):
		attach = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		attach2 = Attachment (self.page)
		self.assertTrue (attach != attach2)
		self.assertEqual (len (attach2.attachmentFull), len (self.fullFilesPath))

		attachBasenames = [os.path.basename (path) for path in attach2.attachmentFull]

		for path in self.fullFilesPath:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)


	def testRemoveAttachesEvent (self):
		attach = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		Application.onPageUpdate += self.onPageUpdate

		attach.removeAttach ([self.files[0]])

		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath) - 1)
		self.assertEqual (self.pageUpdateCount, 1)
		self.assertEqual (self.pageUpdateSender, self.page)


		attach.removeAttach ([self.files[1], self.files[2] ])
		
		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath) - 3)
		self.assertEqual (self.pageUpdateCount, 2)
		self.assertEqual (self.pageUpdateSender, self.page)
		
		Application.onPageUpdate -= self.onPageUpdate


	def testRemoveAttaches1 (self):
		attach = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		attach.removeAttach ([self.files[0]])

		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath[1:]) )

		attachBasenames = [os.path.basename (path) for path in attach.attachmentFull]

		for path in self.fullFilesPath [1: ]:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)


		for path in attach.attachmentFull:
			self.assertTrue (os.path.exists (path))


	def testRemoveAttaches2 (self):
		attach = Attachment (self.page)
		attach2 = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		attach.removeAttach ([self.files[0]])

		self.assertEqual (len (attach2.attachmentFull), len (self.fullFilesPath[1:]) )

		attachBasenames = [os.path.basename (path) for path in attach2.attachmentFull]

		for path in self.fullFilesPath [1: ]:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)


	def testRemoveAttaches3 (self):
		attach = Attachment (self.page)
		attach2 = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		attach2.removeAttach ([self.files[0]])

		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath[1:]) )
		self.assertEqual (len (attach2.attachmentFull), len (self.fullFilesPath[1:]) )

		attachBasenames = [os.path.basename (path) for path in attach.attachmentFull]

		for path in self.fullFilesPath [1: ]:
			self.assertTrue (os.path.basename (path) in attachBasenames, path)


	def testRemoveAttachDir1 (self):
		attach = Attachment (self.page)

		attach.attach (self.fullFilesPath)

		attach.removeAttach ([u"dir"])

		self.assertEqual (len (attach.attachmentFull), len (self.fullFilesPath[1:]) )


	def testInvalidRemoveAttaches (self):
		"""
		Попытка удалить прикрепления, которого нет
		"""
		attach = Attachment (self.page)
		files = [u"accept_111.png", u"add.png_111", u"anchor.png_111"]

		self.assertRaises (IOError, attach.removeAttach, files)
		self.assertRaises (IOError, attach.removeAttach, [u"dir_111"])

