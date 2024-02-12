# Alternate History

**Category**: Crypto\

**Author**: Brad M\

**Difficulty**: Hard\

### Description
It's 1946 and Allied Enigma machine code-breaking efforts have been uncovered. This has forced a considerable alteration to its internal design.

Read the intelligence report and decipher the associated message before it is too late!

Note: You will need to wrap the flag with `UACTF{...}`.

### Solution

Implement a 12-rotor cipher machine similar to an Enigma machine. See enigma.py for what I implemented.
- A known plaintext attack could work, but in this case there is nothing known about the message prior to encryption, so statistics might be a difficult path to take. There is no, "Heil bloody Hitler" in this message!
- There is no reflector on this version of the enigma, so the electrical signal does not travel back through each rotor. Thus to decipher messages, the signal must flow through the device in reverse.
- The first rotor turns on every key press.
- Each rotor following only clicks once for every rotation of the rotor prior.
- There are no internal ring settings for the rotors, only initial positions for them to be set to.
- Each rotor will turn if it needs to before allowing a letter to be encrypted. Thus if rotor 1 is on setting 'A', it will turn to 'B' then encrypt.
- The plugboard substitution applies to the plaintext characters before anything is encrypted. As the machine is no longer symmetric in its encryption, this operation must be done last when decrypting.
- Although not explicitly stated, the settings used to encrypt the message are those for the 16th of July. This is alluded to in the intelligence report.

**Flag**: `UACTF{WWWDOTDSTDOTDEFENCEDOTGOVDOTAUFORWARDSLASHCAREERS}`