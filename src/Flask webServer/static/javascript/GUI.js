$(function() {
    $('#forward').click(function() {
        $.ajax({
            url: '/companion/forward',
            type: 'get',
        })
    })
    
    $('#left').click(function() {
        $.ajax({
            url: '/companion/left',
            type: 'get',
        })
    })

    $('#stop').click(function() {
        $.ajax({
            url: '/companion/stop',
            type: 'get',
        })
    })

    $('#right').click(function() {
        $.ajax({
            url: '/companion/right',
            type: 'get',
        })
    })

    $('#backward').click(function() {
        $.ajax({
            url: '/companion/backward',
            type: 'get',
        })
    })
})