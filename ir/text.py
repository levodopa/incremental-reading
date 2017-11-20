#EXPERIMENTAL 4.7.14
from collections import defaultdict

from anki.notes import Note
from aqt import mw
from aqt.addcards import AddCards
from aqt.editcurrent import EditCurrent
from aqt.utils import getText, showInfo, tooltip

from .util import fixImages, getField, setField

SCHEDULE_EXTRACT = 0


class TextManager:
    def __init__(self):
        self.history = defaultdict(list)

    def highlight(self, bgColor=None, textColor=None, classValue=None):
        if not classValue: 
            classValue = "normal"
        script = "highlight('%s', '%s', '%s');" % (bgColor, textColor, classValue)
        mw.web.eval(script)
        self.save()

    def tag(self):
        hashtag = None
        self.addTag(hashtag)

    def tag_algorithm(self):
        hashtag = "algorithm"
        self.addTag(hashtag)

    def tag_definition(self):
        hashtag = "definition"
        self.addTag(hashtag) 

    def tag_important(self):
        hashtag = "important"
        self.addTag(hashtag)
   
    def tag_diagnostic(self):
        hashtag = "diagnostic"
        self.addTag(hashtag)

    def tag_illness(self):
        hashtag = "illness"
        self.addTag(hashtag)

    def tag_lab_value(self):
        hashtag = "lab_value"
        self.addTag(hashtag)

    def tag_pathogen(self):
        hashtag = "pathogen"
        self.addTag(hashtag)
        
    def tag_pill(self):
        hashtag = "pill"
        self.addTag(hashtag)

    def tag_symptom(self):
        hashtag = "symptom"
        self.addTag(hashtag)

    def tag_treatment(self):
        hashtag = "treatment"
        self.addTag(hashtag)

    def addTag(self, hashtag):
        currentCard = mw.reviewer.card
        currentNote = currentCard.note()
        currentTags = currentNote.tags     

        if not mw.web.selectedText():
             if hashtag == None:
                showInfo('Please select a text to add a tags.')
                return
             else :
                new_tag = '#'+hashtag 
                if new_tag in currentTags:
                    currentTags.remove(new_tag)
                    showInfo('Removed "'+ new_tag + '" from tags!\n\t'+ str(currentTags))
                else : 
                    currentTags.append(new_tag)
                    showInfo('Added "'+ new_tag + '" to tags!\n\t'+ str(currentTags)) 
        else: 
            selection = mw.web.selectedText()
            selection = selection.replace("en ", "e ") # for German tags to singular form
            selection = selection.strip().replace(" ", "_")
            if hashtag == None:
                new_tag = selection
                script = "markTags('%s');" % ('tagged')
            else : 
                new_tag = '#'+hashtag+'::'+selection
                script = "markTags('%s');" % ('tagged '+ hashtag)
            if new_tag not in currentTags:
                currentTags.append(new_tag)
                mw.web.eval(script)
                showInfo('Added "'+ new_tag + '" to tags:\n\t' +str(currentTags))
            else:
                mw.web.eval(script)
                showInfo("Tag has already been added!")
        self.save()

    def bold(self):
        script = "format('%s');" % ("bold")
        mw.web.eval(script)
        self.save()

    def underline(self):
        script = "format('%s');" % ("underline")
        mw.web.eval(script)
        self.save()

    def italics(self):
        script = "format('%s');" % ("italics")
        mw.web.eval(script)
        self.save()

    def strikethrough(self):
        script = "format('%s');" % ("strikethrough")
        mw.web.eval(script)
        self.save()

    def extract(self):
        if not mw.web.selectedText():
            showInfo('Please select some text to extract.')
            return
        if self.settings['plainText']:
            mw.web.evalWithCallback('getPlainText()', self.create)
        else:
            mw.web.evalWithCallback('getHtmlText()', self.create)

    def create(self, text):
        classValue = "extract"
        self.highlight(self.settings['extractBgColor'], 
                       self.settings['extractTextColor'], 
                       classValue)

        currentCard = mw.reviewer.card
        currentNote = currentCard.note()
        model = mw.col.models.byName(self.settings['modelName'])
        newNote = Note(mw.col, model)
        newNote.tags = currentNote.tags

        setField(newNote, self.settings['textField'], fixImages(text))
        setField(newNote,
                 self.settings['sourceField'],
                 getField(currentNote, self.settings['sourceField']))

        if self.settings['editSource']:
            EditCurrent(mw)

        if self.settings['extractDeck']:
            did = mw.col.decks.byName(self.settings['extractDeck'])['id']
        else:
            did = currentCard.did

        if self.settings['copyTitle']:
            title = getField(currentNote, self.settings['titleField'])
        else:
            title = ''

        if self.settings['editExtract']:
            setField(newNote, self.settings['titleField'], title)
            addCards = AddCards(mw)
            addCards.editor.setNote(newNote)
            deckName = mw.col.decks.get(did)['name']
            addCards.deckChooser.deck.setText(deckName)
            addCards.modelChooser.models.setText(self.settings['modelName'])
        else:
            title, accepted = getText('Enter title',
                                      title='Extract Text',
                                      default=title)
            if accepted:
                setField(newNote, self.settings['titleField'], title)
                newNote.model()['did'] = did
                mw.col.addNote(newNote)

        if self.settings['extractSchedule']:
            cards = newNote.cards()
            if cards:
                mw.readingManager.scheduler.answer(cards[0], SCHEDULE_EXTRACT)

    def remove(self):
        mw.web.eval('removeText()')
        self.save()

    def undo(self):
        note = mw.reviewer.card.note()

        if note.id not in self.history or not self.history[note.id]:
            showInfo('No undo history for this note.')
            return

        note['Text'] = self.history[note.id].pop()
        note.flush()
        mw.reset()
        tooltip('Undone')

    def save(self):
        def callback(text):
            if text:
                note = mw.reviewer.card.note()
                self.history[note.id].append(note['Text'])
                note['Text'] = text
                note.flush()

        mw.web.evalWithCallback(
            'document.getElementsByClassName("ir-text")[0].innerHTML;',
            callback)
