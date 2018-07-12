from pushbullet.pushbullet import PushBullet


class BotLog(object):
	def __init__(self):
		self.apiKey = ""

	def log(self, message):
		print (message)

	def sendNotif(self,header,body):
		if self.apiKey == "":
			fichier = open("api.txt","r")
			self.apiKey = fichier.read()[:-1] # attention retour a la ligne
			fichier.close()

		p = PushBullet(self.apiKey)
		devices = p.getDevices()
		for i in range(len(devices)):
			p.pushNote(devices[i]["iden"], header, body)



		# # Get a list of devices
		# devices = p.getDevices()
        #
		# # Get a list of contacts
		# contacts = p.getContacts()
        #
		# Send a note
		# p.pushNote(devices[0]["iden"], 'Hello world', 'Test body')
		#
		# # Send a map location
		# p.pushAddress(devices[0]["iden"], "Eiffel tower", "Eiffel tower, france")
		#
		# # Send a list
		# p.pushList(devices[0]["iden"], "Groceries", ["Apples", "Bread", "Milk"])
		#
		# # Send a link
		# p.pushLink(devices[0]["iden"], "Google", "http://www.google.com")
		#
		# # Send a file
		# p.pushFile(devices[0]["iden"], "file.txt", "This is a text file", open("file.txt", "rb"))
		#
		# # Send a note to a channel
		# p.pushNote('channel_tag', 'Hello world', 'Test body', recipient_type='channel_tag')
		#
		# # Send a note to an email
		# p.pushNote('myemail@domain.com', 'Hello world', 'Test body', recipient_type='email')
