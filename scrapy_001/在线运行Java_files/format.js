var formatJson = {
    html: true,
    javascript: true
};

function formatShow(type){
    if (formatJson[type]) {
        $('#format').show()
    } else {
        $('#format').hide()
    }
}

function formatCode (type) {
    if (type==='HTML'||type==='javasSript') {
        return true
    } else {
        return false
    }
}