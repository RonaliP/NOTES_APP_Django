from django.urls import path
from django.conf.urls import url
from Notes.views import CreateandListNotes,NoteDetails, CreateAndDisplayLabels, LabelDetails, ArchiveNote, NoteToTrash, \
    ArchiveNotesList, TrashList, AddLabelsToNote, ListNotesInLabel,Notesearch,AddCollaboratorForNotes,notesreminder,DeleteNote

urlpatterns = [

    path('notes/',CreateandListNotes.as_view() , name='notecreation'),
    path('note/<int:id>',NoteDetails.as_view() , name='note'),
    path('delete-note/<int:id>', DeleteNote.as_view(), name='delete-note'),
    path('labels/',CreateAndDisplayLabels.as_view() , name='labels'),
    path('label/<int:id>',LabelDetails.as_view() , name='label'),
    path('archive-note/<int:id>', ArchiveNote.as_view(), name='archive-note'),
    path('note-to-trash/<int:id>',NoteToTrash.as_view(), name='note-to-trash'),
    path('archive-list/', ArchiveNotesList.as_view(), name='archive-list'),
    path('trash-list/',TrashList.as_view(), name='trash-list'),
    path('add-label/<int:note_id>', AddLabelsToNote.as_view(), name='add-label'),
    path('list-notes-in-label/<int:label_id>', ListNotesInLabel.as_view(), name='list-notes-in-label'),
    path('search/', Notesearch.as_view(), name='search'),
    path('collaborator/<int:note_id>', AddCollaboratorForNotes.as_view(), name='collaborator'),
    path('reminder/<int:note_id>', notesreminder.as_view(), name='reminder'),
]

