/// <reference path="../jquery-3.5.1.min.js" />

$(function () {
    $('#btn1').click(async function (e) {
        e.preventDefault()

        $('#el_response1').html('...loading')

        let ogrn = $('#ogrn').val()

        let h = $(this).attr('href')

        try {

            let d = await $.get(h+'?ogrn='+ogrn)

            console.warn('d', d)

            d = JSON.stringify(d, null, 4)

            $('#el_response1').html(d)

        } catch (err) {
            console.error(err)
            $('#el_response1').text('ERROR"\n' + err.responseText)
        }

        return false
    })
})