from django.urls import path
from django.conf.urls import url
from Notes.views import CreateNotes,DisplayNotes, NoteDetails, CreateAndDisplayLabels, LabelDetails, ArchiveNote, NoteToTrash, \
    ArchiveNotesList, TrashList, AddLabelsToNote, ListNotesInLabel,Notesearch

urlpatterns = [
    path('notes/', CreateNotes.as_view(), name='notecreation'),
    path('notesdisplay/', DisplayNotes.as_view(), name='notedisplay'),
    path('SEARCHNOTES/', Notesearch.as_view(), name='notesearchby(title)'),
    path('notedelete/update/retrieve/<int:id>', NoteDetails.as_view(), name='notesdelete/update/retrieve'),
    path('add-label/<int:id>', AddLabelsToNote.as_view(), name='add-label'),
    path('labels/', CreateAndDisplayLabels.as_view(), name='labels'),
    path('labeldelete/update/retrieve/<int:id>', LabelDetails.as_view(), name='labelsdelete/update/retrieve'),
    path('archive-note/<int:id>', ArchiveNote.as_view(), name='archive-note'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('note-to-trash/<int:id>', NoteToTrash.as_view(), name='Sendnote-to-trash'),
    path('trash-list/', TrashList.as_view(), name='trash-list'),
    path('list-notes-in-label/<int:id>', ListNotesInLabel.as_view(), name='list-notes-in-label'),

]