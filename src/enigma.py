# Custom Enigma Machine implementation 
# By Brad Morgan 2022
# UofA CTF Club Event July 2022

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Rotor description object, can't be changed.
class rotor(object):
	def __init__(self, substitution_str, setting):
		self.substitution = substitution_str
		self.setting = ord(setting)-65

#Rotors turns as the key is pressed, not after
#This enigma has no reflector, ruh roh
#Rotors turn after a full rotation
#There are no ring settings, just bare rotors
class enigma:
	def __init__(self, rotors, plugboard):
		#Each rotor is a custom substitution cipher
		self.rotors = rotors

		#Used to calculate how far the rotor has turned
		self.rotors_turn = []
		for r in self.rotors:
			self.rotors_turn.append(r.setting)

		#Substitution for combinations of letters. Given as a string.
		self.plugboard = plugboard

	#Reset rotors to initial turns
	def reset_rotors(self):
		for r in range(0, len(self.rotors)):
			self.rotors_turn[r] = self.rotors[r].setting

	#Each Rotor turns towards operator, thus substitution string "shifts" left and wraps around
	#First rotor turns on every key press. Rotor n turns after each full rotation of the prior rotor
	def turn_rotor(self, r):
		if(r == 0):
			#Turn on every key press
			self.rotors_turn[r] += 1
			#Full rotation, so turn next rotor and reset back to 0
			if(self.rotors_turn[r] == 26):
				self.rotors_turn[r] = 0
				if(len(self.rotors) > 1):
					self.rotors_turn[r+1] += 1
		else:
			#Full rotation, turn next rotor and reset back to 0
			if(self.rotors_turn[r] == 26):
				self.rotors_turn[r] = 0
				#Last rotor has nothing to turn
				if(r != len(self.rotors)-1):
					self.rotors_turn[r+1] += 1

	#Substitute the letter using the rotor. Python Char/Integer shenanigans abound.
	def rotor_encipher(self, n, r):
		offset = (n + self.rotors_turn[r]) % 26
		sub = ord(self.rotors[r].substitution[offset])-65
		return sub

	def rotor_decipher(self, n, r):
		sub = 0
		#Find character in the rotor matching n
		for c in range(0, len(self.rotors[r].substitution)):
			if(n == ord(self.rotors[r].substitution[c])-65):
				#Reverse the operation, taking into consideration the turn
				sub = (c - self.rotors_turn[r]) % 26
		#If we are at the first rotor, convert to alphabet.
		if(r == 0):
			sub = ord(alphabet[sub])-65
		return sub

	#Substitute letters according to provided plugboard settings
	def plugboard_substitute(self, p):
		substituted = ""
		for c in p:
			n = ord(c)-65
			substituted += self.plugboard[n]
		return substituted

	def encipher(self, p):
		self.reset_rotors()
		ciphertext = ""

		plugboard_p = self.plugboard_substitute(p)

		for key in plugboard_p:
			#Convert current letter to a number from 0-25
			sub = ord(key)
			sub = sub - 65

			for r in range(0, len(self.rotors)):
				#Operator presses down key n, rotors turn
				#This cascades through each rotor
				self.turn_rotor(r)

			for r in range(0, len(self.rotors)):
				#Then, substitution occurs
				sub = self.rotor_encipher(sub, r)

			ciphertext += chr(sub+65)
		return ciphertext

	def decipher(self, c):
		self.reset_rotors()
		plaintext = ""

		for key in c:
			#Convert current letter to a number from 0-25
			sub = ord(key)
			sub = sub - 65

			#Operator presses down key n, rotors turn
			#This cascades through each rotor
			for r in range(0, len(self.rotors)):
				self.turn_rotor(r)

			#Reverse rotor operations, start from last rotor
			for r in range(len(self.rotors)-1, -1, -1):
				#Substitution occurs
				sub = self.rotor_decipher(sub, r)

			plaintext += chr(sub+65)
		#Run plaintext back through the plugboard and output
		plaintext = self.plugboard_substitute(plaintext)
		return plaintext


def main():
	test_text = alphabet
	flag = "DEUTSCHESIPSUMDOLORDESERUNTSCHWEINSTEIGERHASANWENDUNGSPROGRAMMIERSCHNITTSTELLETOLLITJUTTENSACKIUSSPEZISAEPESCHNAPSELABORARETSCHMETTERLINGNEGESUNDHEITEUKAFTFAHRZEUGHAFTPFLICHTVERSICHERUNGPERTINAXAUDIERIPUITCURRYWURSTNOCURRYWURSTDIAMUEBERNOFERNWEHEOSFREUDESCHOENERGOETTERFUNKENSUSCIPITKAESEFONDUEEAMBITTEOFFENDITHELMUTKOHLADGENAUVOLUPTATIBUSSCHMETTERLINGADAPFELSCHORLECONSULMETTWURSTVIXFREUDESCHOENERGOETTERFUNKENQUASSCHNAPSVERITUSSCHNELLLATINEANWENDUNGSPROGRAMMIERSCHNITTSTELLECOMPLECTITURPFANNKUCHENMEALEBKUCHENDENIQUEMICHAELSCHUHMACHERIDFRAUPROFESSOREXPETENDAEICHHOERNCHENANFUSSBALLEIDOPPELSCHERENHUBTISCHWAGENEUISMODPROJEKTPLANUNGODIOFREUDESCHOENERGOETTERFUNKENIRACUNDIAOHRWURMPRIHANDTASCHEVELZAUBERERMANDAMUSREISENATUMPROSTEIANWENDUNGSPROGRAMMIERSCHNITTSTELLEDIAMNEUNUNDNEUNZIGLUFTBALLONSHONESTATISSCHWEINSTEIGERNOMELIOREFRAUPROFESSORETGENAUTEGUTENTAGUTAMURDIETOTENHOSENEXERCIBREZELEUGOETHEPRINCIPESBERLINEOSBITTEHISMERCEDESBENZMODERATIUSMILKAATFUSSBALLWELTMEISTERSCHAFTOMNISRIESLINGEPICUREIANWENDUNGSPROGRAMMIERSCHNITTSTELLEFEUGAITSIEBENTAUSENDZWEIHUNDERTVIERUNDFUENFZIGEISPEZIPURTOGLUEHWEINTESITGRIMMSMAERCHENCONSECTETURKAESEFONDUEELITERBSENZAEHLERDOENTSCHULDIGUNGTEMPORAUFENTHALTSGENEHMIGUNGUTBERLINETKAESEFONDUEMAGNAHAMBURGUTDEUTSCHEMARKADHONIGKUCHENPFERDVENIAMWARMDUSCHERNOSTRUDMOZARTULLAMCOBITTENISIWEIHNACHTENALIQUIPGUTENTAGEABIERCONSEQUATSCHMETTERLINGAUTEDONAUDAMPFSCHIFFAHRTSGESELLSCHAFTSKAPITAENDOLORBITTEREPREHENDERITOKTOBERFESTVOLUPTATEBRATWURSTESSESCHWEINSTEIGERDOLOREWIEGEHTSFUGIATAUDIPARIATURKREUZBERGSINTKINDERGARTENCUPIDATATFUSSBALLWELTMEISTERSCHAFTPROIDENTFROHSINNINNACKENHEIMQUIGLUEHWEINDESERUNTLUKASPODOLSKIANIMAPFELSTRUDELESTAPFELSCHORLELUCILIUSFREUDESCHOENERGOETTERFUNKENATHALLOLABORAMUSTURNBEUTELPERMERTESACKERINZAUBERERULLUMPROSTIDDIEAERZTERECTEQUEMILCHREISSEDDIEUNENDLICHEGESCHICHTENECWIENERSCHNITZELARGUMENTUMHERRDOKTORMELIUSWELTVIXHANDTASCHEUTSCHWARZWAELDERKIRSCHTORTECAUSAEJUTTENSACKPRODESSETAUFENTHALTSGENEHMIGUNGMEAKIRSCHKERNEDICUNTAPEROLSPRITZSUSCIPITSTUTTGARTNOGEMEINSAMKEITNEMOREHERRDOKTOREUMMOZARTREGIONEWIENERSCHNITZELEFFICIENDIAUDITTTTTTTTDIEFLAGGEISTTTTTTTTWWWDOTDSTDOTDEFENCEDOTGOVDOTAUFORWARDSLASHCAREERS"
	rotors = []
	rotors.append(rotor("NHRMEWUKBQXAOLVJTPYDIGFZSC", "E")) # I
	rotors.append(rotor("LQGYZRUMSWKOTEVDNFACHXBIJP", "H")) # III
	rotors.append(rotor("TYCXZOSFDWPBRHLKUQJAVEINMG", "J")) # II
	rotors.append(rotor("ZAJGKUOYDTHLRVFNQSIWBEPXMC", "P")) # XI
	rotors.append(rotor("KHSWDIGFXVETMYRUCJPLNOBAZQ", "B")) # X
	rotors.append(rotor("THPBSEQJUNVGLOKZWCRMAYFDIX", "R")) # VIII
	rotors.append(rotor("RMUDCXFOWTYJZKIEAHSVLPNGBQ", "O")) # IV
	rotors.append(rotor("SPIQJDZWKCHRFUYXOTLGVBNMAE", "M")) # VI
	rotors.append(rotor("CRADPXJUGZQINKLESMOVYHFTWB", "Q")) # V
	rotors.append(rotor("SBCUWMEXPQYGJVNRDKZTOLIHAF", "X")) # IX
	rotors.append(rotor("JWGEAFLOIZHPVQKMDSBCRYUTNX", "W")) # VII
	rotors.append(rotor("HAVBWPOKNXMICJTSFQDEGURYLZ", "D")) # XII

	#AF HY OP BR EU MZ CT IL KW QV
	plugboard_settings = "FRTDUAGYLJWIZNPOVBSCEQKXHM"

	print("Message:\n%s" % flag, end="\n\n")

	e = enigma(rotors, plugboard_settings)
	ciphertext = e.encipher(flag)
	print("Enciphered:\n%s" % ciphertext, end="\n\n")

	result = e.decipher(ciphertext)
	print("Deciphered:\n%s" % result)


		
if __name__ == '__main__':
	main()