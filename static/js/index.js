(function () {
    $(document).ready(function () {
        var allFlashcards = [];
        var flashcards = [];
        var image = $('#flashcard-image');
        var answer = $('#flashcard-answer');
        var currentCard = null;

        function showRandomFlashcard() {
            if(flashcards.length == 0) {
                flashcards = _.shuffle(allFlashcards);
            }
            currentCard = flashcards.pop();
            image.attr('src', currentCard['image']);
            answer.text('');
        }

        function showAnswer() {
            answer.text(currentCard['answer']);
        }

        function bindAnswerButton() {
            $('#show-answer-btn').click(function(e) {
                e.preventDefault();
                showAnswer();
                setTimeout(function() {
                    showRandomFlashcard();
                }, 2500)
            });
        }

        $.ajax({
            type: 'GET',
            url: '/flashcards',
            timeout: 15000,
            success: function (data, textStatus, jqXHR) {
                allFlashcards = data['flashcards'];
                bindAnswerButton();
                showRandomFlashcard();
            },
            error: function (e) {
                alert(e);
            }
        });
    });

})();
