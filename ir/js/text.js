//EXPERIMENTAL 4.7.14

function highlight(bgColor, textColor, classValue) {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = selection.extractContents();
    var span = document.createElement("span");
    span.className = "ir-highlight " + classValue;
    span.setAttribute("ir-overlay", "on");
    span.appendChild(selectedText);
    //var styleSheet = document.styleSheets[0];
    //css_rule = '[ir-overlay~="on"].ir-highlight.' + classValue +
    //    "{ color: " + textColor + "; background-color: " + bgColor +";}";
    //styleSheet.insertRule(css_rule);
    selection.insertNode(span);
}

function markTags(hashtag) {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = selection.extractContents();
    var span = document.createElement("span");
    span.className = "ir-highlight " + hashtag;
    span.setAttribute("ir-overlay", "on");
    span.appendChild(selectedText);
    selection.insertNode(span);
}


function format(classValue) {
    var selection = window.getSelection().getRangeAt(0);
    var selectedText = selection.extractContents();
    var span = document.createElement("span");
    span.className = "ir-highlight " + classValue;
    span.setAttribute("ir-overlay", "on");
    span.appendChild(selectedText);

    selection.insertNode(span);
}

function removeText() {
    var range, sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
        range = sel.getRangeAt(0);
        var startNode = document.createElement('span');
        range.insertNode(startNode);
        var endNode = document.createElement('span');
        range.collapse(false);
        range.insertNode(endNode);
        range.setStartAfter(startNode);
        range.setEndBefore(endNode);
        sel.addRange(range);
        range.deleteContents();
    }
}

function getPlainText() {
    return window.getSelection().toString();
}

function getHtmlText() {
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);
    var div = document.createElement('div');
    div.appendChild(range.cloneContents());
    return div.innerHTML;
}
