function getBase64(file) {
    // Hi i copypasted this code and i have no idea what i'm doing
    // I hope this will suffice for 1 point since i don't think i can take
    // any more JavaScript
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $('.custom-file-input').on('change', function () {
        if ($(this).val()) {
            let fileName = $(this).val().match(/[/\\]([^/\\]+)$/)[1];
            $(this).next('.custom-file-label').html(fileName);
        }
    });

    const loginForm = '[data-js=form-login]';
    const logoutForm = '[data-js=form-logout]';
    const signupForm = '[data-js=form-signup]';
    const answerForm = '[data-js=answer_form]';
    const questionCreateForm = '[data-js=question-create]';
    const profileEditForm = '[data-js=user-edit]';
    const csrfToken = $.cookie('csrftoken');

    $(profileEditForm).on('submit', function (event) {
        event.preventDefault();
        const $this = $(this)[0];
        const data = new FormData($this);
        console.log($this);
        for (let e of data.entries())
            console.log(e);
        const action = $this['action'];
        $.ajax({
            url: action,
            data: data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        $(`input[id=id_${elem}`).addClass('is-invalid').show();
                        $(`#id_${elem}-help`).addClass('alert-danger').text(response['errors'][elem][0]).show();
                        $(`label[for=id_${elem}`).addClass('text-danger').show();
                    }

                }
            $(`#edit_profile_help`).text('Please, fix the errors above!').show();
            console.log(response);
        })
    });

    /*$(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
        $('.custom-file-input').on('change', function () {
            if ($(this).val()) {
                let fileName = $(this).val().match(/[/\\]([^/\\]+)$/)[1];
                $(this).next('.custom-file-label').html(fileName);
            }
        });

        const loginForm = '[data-js=form-login]';
        const logoutForm = '[data-js=form-logout]';
        const signupForm = '[data-js=form-signup]';
        const answerForm = '[data-js=answer_form]';
        const questionCreateForm = '[data-js=question-create]';
        const profileEditForm = '[data-js=user-edit]';
        const csrfToken = $.cookie('csrftoken');

        $(profileEditForm).on('submit', function (event) {
            event.preventDefault();
            const $this = $(this);
            const data = new FormData($this[0]);
            data.delete('upload');
            const $upload = $('#id_upload');
            if ($upload.prop('files')[0])
                getBase64($upload.prop('files')[0]).then(b64 => {
                    data.append('upload', b64);
                    for (x of data.entries()) {
                        console.log(x);
                    }
                    console.log(b64);
                });
            const action = $this.attr('action');
            console.log($this);
            console.log(this);

            $.ajax({
                url: action,
                data: data,
                processData: false,
                contentType: false,
                type: 'POST'
            }).done(function (response) {
                if (response['status'] === 'OK')
                    window.location = response['success_url'];
                else
                    for (const elem in response['errors']) {
                        if (response['errors'].hasOwnProperty(elem)) {
                            $(`input[id=id_${elem}`).addClass('is-invalid').show();
                            $(`#id_${elem}-help`).addClass('alert-danger').text(response['errors'][elem][0]).show();
                            $(`label[for=id_${elem}`).addClass('text-danger').show();
                        }

                    }
                $(`#edit_profile_help`).text('Please, fix the errors above!').show();
                console.log(response);
            })
        });*/

    /*$(profileEditForm).on('submit', function(event) {
        event.preventDefault();
        const $this = $(this);
        const action = $this.attr('action');
        const data = $this.serialize();
        const img = new FormData();
        const file_input = $('input[id=id_upload]');
        if (file_input.files.length)
            img.append('upload', $(file_input).files[0]);

        $.post(action, data).done(function(response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        $(`input[id=id_${elem}`).addClass('is-invalid').show();
                        $(`#id_${elem}-help`).addClass('alert-danger').text(response['errors'][elem][0]).show();
                        $(`label[for=id_${elem}`).addClass('text-danger').show();
                    }

                }
                $(`#edit_profile_help`).text('Please, fix the errors above!').show();
            console.log(response);
        })
    })*/
    ;

    $(loginForm).on('submit', function (event) {
        event.preventDefault();
        const $this = $(this);
        const action = $this.attr('action');
        const data = $this.serialize();
        $.post(action, data).done(function (response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        $(`input[id=id_login_${elem}`).addClass('is-invalid');
                        $(`label[for=id_login_${elem}`).addClass('text-danger');
                        $(`#login-form-help`).addClass('text-danger').text(response['errors'][elem][0]).show();
                    }
                }
            console.log(response);
        });
    });

    $(logoutForm).on('click', function (event) {
        event.preventDefault();

        const href = $(this).attr('href');
        $.get(href).done(function (response) {
            if (response['status'] === 'OK') {
                window.location = response['success_url'];
            }
        })
    });

    $(signupForm).on('submit', function () {
        event.preventDefault();
        const $this = $(this);
        const action = $this.attr('action');
        let data = $this.serialize();
        data += "&password1=" + $('#id_password').val();
        $.post(action, data).done(function (response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        $(`input[id=id_${elem}`).addClass('is-invalid');
                        $(`label[for=id_${elem}`).addClass('text-danger');
                        $(`.form-help[id=id_${elem}-help]`).addClass('text-danger').text(response['errors'][elem][0]).show();
                    }
                }
            console.log(response);
        });
    });

    $(questionCreateForm).on('submit', function () {
        event.preventDefault();
        const $this = $(this);
        const action = $this.attr('action');
        console.log(action);
        let data = $this.serialize();
        $.ajax({
            url: action,
            data: data,
            type: 'post',
            headers: {'X-CSRFToken': csrfToken},
        }).done(function (response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        console.log(`.form-help[id=id_${elem}-help]`);
                        $(`input[id=id_${elem}`).addClass('is-invalid');
                        $(`label[for=id_${elem}`).addClass('text-danger');
                        $(`.form-help[id=id_${elem}-help]`).addClass('text-danger').text(response['errors'][elem][0]).show();
                    }
                }
            console.log(response);
        });
    });

    $(answerForm).on('submit', function () {
        event.preventDefault();
        const $this = $(this);
        const action = $this.attr('action');
        console.log(action);
        let data = $this.serialize();
        $.post(action, data).done(function (response) {
            if (response['status'] === 'OK')
                window.location = response['success_url'];
            else
                for (const elem in response['errors']) {
                    if (response['errors'].hasOwnProperty(elem)) {
                        console.log(`.form-help[id=id_${elem}-help]`);
                        $(`input[id=id_answer_${elem}`).addClass('is-invalid');
                        $(`label[for=id_answer_${elem}`).addClass('text-danger');
                        $(`.form-help[id=id_answer_${elem}-help]`).addClass('text-danger').text(response['errors'][elem][0]).show();
                    }
                }
            console.log(response);
        });
    });

    const questionUpvote = '[data-js="question-upvote"]';
    const questionDownvote = '[data-js="question-downvote"]';

    $(questionUpvote).on('click', function () {
        event.preventDefault();
        const $this = $(this);
        const url = $this.attr('data-url');
        console.log(csrfToken);
        $.post(url, {'csrfmiddlewaretoken': csrfToken}, function (response) {
            if (response['status'] === 'OK') {
                let $rating = $(`[data-js="question-rating-${$this.attr('data-id')}"]`);
                $rating.text(` ${parseInt($rating.text()) + 1} `);
            }

            console.log(response);
        })
    });

    $(questionDownvote).on('click', function () {
        event.preventDefault();
        const $this = $(this);
        const url = $this.attr('data-url');
        $.post(url, {'csrfmiddlewaretoken': csrfToken}, function (response) {
            if (response['status'] === 'OK') {
                let $rating = $(`[data-js="question-rating-${$this.attr('data-id')}"]`);
                $rating.text(` ${parseInt($rating.text()) - 1} `);
            }

            console.log(response);
        })
    });

    const answerUpvote = '[data-js="answer-upvote"]';
    const answerDownvote = '[data-js="answer-downvote"]';

    $(answerUpvote).on('click', function () {
        event.preventDefault();
        const $this = $(this);
        const url = $this.attr('data-url');
        console.log(csrfToken);
        $.post(url, {'csrfmiddlewaretoken': csrfToken}, function (response) {
            if (response['status'] === 'OK') {
                let $rating = $(`[data-js="answer-rating-${$this.attr('data-id')}"]`);
                $rating.text(` ${parseInt($rating.text()) + 1} `);
            }

            console.log(response);
        })
    });

    $(answerDownvote).on('click', function () {
        event.preventDefault();
        const $this = $(this);
        const url = $this.attr('data-url');
        $.post(url, {'csrfmiddlewaretoken': csrfToken}, function (response) {
            if (response['status'] === 'OK') {
                let $rating = $(`[data-js="answer-rating-${$this.attr('data-id')}"]`);
                $rating.text(` ${parseInt($rating.text()) - 1} `);
            }

            console.log(response);
        })
    });
});