function downloadZipRunCode(name, value) {
    var blob = new Blob([value], {type: ''});
    saveAs(blob, name);
}

//语言切换
$('#lang a').click(function () {
    var txt = $(this).text();
    $(this).parents('.input-group-btn').find('button .txt').eq(0).text(txt)
});

//点击运行代码
$('#runCode').click(function () {
    if ($(this).hasClass('disabled')) {
        return;
    }
    $(this).button('loading');
    $('#putBoxOutput').show();
    codeRun();
});


//主编辑器最大化
$('#aceEditorMax').click(function () {
    var type = $(this).attr('data-max');
    $('#containerHalfScreen').toggleClass('widthandmaxwidth-100');
    if (type === 'no') {
        $('#containerHalfScreen').css('height', 'auto');
        $(this).attr('data-max', 'yes');
        $('#aceEditorContain').height(windowHeight);
        $('#aceEditorInput').height(windowHeight - 4);
    } else {
        $('#containerHalfScreen').css('height', '');
        $(this).attr('data-max', 'no');
        $('#aceEditorContain').height('');
        $('#aceEditorInput').height('');
    }
    aceEditorInput.resize();
    $(aceEditor).each(function (index, item) {
        item.resize();
    });
});

//下载代码
$('#downloadCode').click(function () {
    var index = $('#aceList .active').index();
    var code = aceEditor[index].getValue();
    var name = $('#aceList .active span').text();
    downloadZipRunCode(name, code);
});

//复制主编辑器代码
new ClipboardJS('#copyMainEditor', {
    text: function (trigger) {
        var index = $('#aceList .active').index();
        var value = aceEditor[index].getValue();
        if (value) {
            msgSuccess('当前代码复制成功');
            return value;
        } else {
            return false;
        }
    }
});

//编辑器设置
$('#setting').click(function () {
    $('#settingModal').modal('toggle', 'fit');
});

//键盘快捷键
$('#shortcubKeybord').click(function () {
    $('#keybordModal').modal('toggle', 0);
});

//左侧行号
$('#lineNumber').change(function () {
    if ($(this).prop('checked')) {
        localStorage.setItem('showGutter', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('showGutter', true);
        });
    } else {
        localStorage.setItem('showGutter', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('showGutter', false);
        });
    }
});

//自动补全
$('#autoComplete').change(function () {
    if ($(this).prop('checked')) {
        localStorage.setItem('enableBasicAutocompletion', '1');
        localStorage.setItem('enableSnippets', '1');
        $(aceEditor).each(function (index, item) {
            item.setOptions({
                enableBasicAutocompletion: true,
                enableSnippets: true,
                enableLiveAutocompletion: true
            });
        });
    } else {
        localStorage.setItem('enableBasicAutocompletion', '0');
        localStorage.setItem('enableSnippets', '0');
        $(aceEditor).each(function (index, item) {
            item.setOptions({
                enableBasicAutocompletion: false,
                enableSnippets: false,
                enableLiveAutocompletion: false
            });
        });
    }

});

//自动换行
$('#lineWarp').change(function () {
    if ($(this).prop('checked')) {
        localStorage.setItem('useWrapMode', '1');
        $(aceEditor).each(function (index, item) {
            item.getSession().setUseWrapMode(true);
        });
    } else {
        localStorage.setItem('useWrapMode', '0');
        $(aceEditor).each(function (index, item) {
            item.getSession().setUseWrapMode(false);
        });
    }

});

//多个标签
$('#mutipleTabs').change(function () {
    if ($(this).prop('checked')) {
        localStorage.setItem('mutipleTabs', '1');
        $('#aceList li').show();
        $('#acePlus').show();
    } else {
        localStorage.setItem('mutipleTabs', '0');
        $('#aceList li').hide();
        $('#acePlus').hide();
    }

});

//缩进类型
$('#softTabs').change(function () {
    if ($(this).prop('checked')) {
        localStorage.setItem('useSoftTabs', '1');
        localStorage.setItem('navigateWithinSoftTabs', '1');
        $(aceEditor).each(function (index, item) {
            item.session.setOptions({useSoftTabs: true, navigateWithinSoftTabs: true});
        });
    } else {
        localStorage.setItem('useSoftTabs', '0');
        localStorage.setItem('navigateWithinSoftTabs', '0');
        $(aceEditor).each(function (index, item) {
            item.session.setOptions({useSoftTabs: false, navigateWithinSoftTabs: false});
        });
    }
});

//数字增减
$('.number-add').click(function () {
    var input = $(this).parents('.number-box').find('input').eq(0);
    var value = parseFloat(input.val());
    var max = parseInt(input.attr('data-max'));
    value++;
    if (value > max) {
        return;
    }
    var type = $(this).attr('data-type');
    if (type === 'softtabs') {
        localStorage.setItem('aceTabSize', value.toString());
        $(aceEditor).each(function (index, item) {
            item.getSession().setTabSize(value);
        });
    } else if(type === 'fontsize') {
        localStorage.setItem('aceFontSize', value.toString());
        $(aceEditor).each(function (index, item) {
            item.setOption('fontSize', value);
        });
    } else {
        localStorage.setItem('printMarginColumn', value.toString());
        $(aceEditor).each(function (index, item) {
            item.setOption('printMarginColumn', value);
        });
    }

    input.val(value);
});
$('.number-delete').click(function () {
    var input = $(this).parents('.number-box').find('input').eq(0);
    var value = parseFloat(input.val());
    var min = parseInt(input.attr('data-min'));
    value--;
    if (value < min) {
        return;
    }
    var type = $(this).attr('data-type');
    if (type === 'softtabs') {
        localStorage.setItem('aceTabSize', value.toString());
        $(aceEditor).each(function (index, item) {
            item.getSession().setTabSize(value);
        });
    } else if(type === 'fontsize') {
        localStorage.setItem('aceFontSize', value.toString());
        $(aceEditor).each(function (index, item) {
            item.setOption('fontSize', value);
        });
    } else {
        localStorage.setItem('printMarginColumn', value.toString());
        $(aceEditor).each(function (index, item) {
            item.setOption('printMarginColumn', value);
        });
    }
    input.val(value);
});

//主题选择
$('#themes').change(function () {
    var value = $(this).val();
    localStorage.setItem('aceTheme', 'ace/theme/' + value);
    $(aceEditor).each(function (index, item) {
        item.setTheme('ace/theme/' + value);
    });
});

//更多设置
$('#moreSetting').click(function () {
    $('#settingModal').modal('toggle', 0);
    $('#moreSettingModal').modal('toggle', 0);
});

//光标样式
$('#cursorStyle').change(function(){
    var value = $(this).val();
    localStorage.setItem('aceCursorStyle', value);
    $(aceEditor).each(function (index, item) {
        item.setOption('cursorStyle', value);
    });
});

//折叠样式
$('#foldStyle').change(function(){
    var value = $(this).val();
    localStorage.setItem('aceFoldStyle', value);
    $(aceEditor).each(function (index, item) {
        item.getSession().setFoldStyle(value);
    });
});

//高亮当前行
$('#highlightActiveLine').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('highlightActiveLine', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('highlightActiveLine', true);
        });
    } else {
        localStorage.setItem('highlightActiveLine', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('highlightActiveLine', false);
        });
    }
});

//高亮选中文本
$('#highlightSelectedWord').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('highlightSelectedWord', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('highlightSelectedWord', true);
        });
    } else {
        localStorage.setItem('highlightSelectedWord', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('highlightSelectedWord', false);
        });
    }
});

//显示不可见字符
$('#showInvisibles').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('showInvisibles', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('showInvisibles', true);
        });
    } else {
        localStorage.setItem('showInvisibles', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('showInvisibles', false);
        });
    }
});

//显示纵向滚动条
$('#hScrollBarAlwaysVisible').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('hScrollBarAlwaysVisible', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('hScrollBarAlwaysVisible', true);
        });
    } else {
        localStorage.setItem('hScrollBarAlwaysVisible', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('hScrollBarAlwaysVisible', false);
        });
    }
});

//显示横向滚动条
$('#vScrollBarAlwaysVisible').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('vScrollBarAlwaysVisible', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('vScrollBarAlwaysVisible', true);
        });
    } else {
        localStorage.setItem('vScrollBarAlwaysVisible', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('vScrollBarAlwaysVisible', false);
        });
    }
});

//显示打印编剧
$('#showPrintMargin').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('showPrintMargin', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('showPrintMargin', true);
        });
    } else {
        localStorage.setItem('showPrintMargin', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('showPrintMargin', false);
        });
    }
});

//是否只读
$('#readOnly').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('aceReadOnly', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('readOnly', true);
        });
    } else {
        localStorage.setItem('aceReadOnly', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('readOnly', false);
        });
    }
});

//实时补全
$('#enableLiveAutocompletion').change(function(){
    if ($(this).prop('checked')) {
        localStorage.setItem('#enableLiveAutocompletion', '1');
        $(aceEditor).each(function (index, item) {
            item.setOption('#enableLiveAutocompletion', true);
        });
    } else {
        localStorage.setItem('#enableLiveAutocompletion', '0');
        $(aceEditor).each(function (index, item) {
            item.setOption('#enableLiveAutocompletion', false);
        });
    }
});

//初始化选择框
$('select.ace-select-runcode').chosen({
    no_results_text: '没有找到',    // 当检索时没有找到匹配项时显示的提示文本
    search_contains: true,         // 从任意位置开始检索
    disable_search_threshold: 10 // 10 个以下的选择项则不显示检索框
});

//初始化代码选择的上次选择
//$('#aceEditorTypeList').val(templateAceType);
//$('#aceEditorTypeList').trigger('chosen:updated');

$('select.ace-select-runcode').on('change', function (e, params) {
    var index = $('#aceList .active').index();
    console.log(params)
    window.location.href=$("#aceEditorTypeList>option:selected").attr('url');
    /*
    aceEditor[index].session.setMode(params.selected);
    templateAceType = params.selected;
    templateType = params.selected.split('/')[2];
    localStorage.setItem('templateAceType', templateAceType);
    localStorage.setItem('templateType', templateType);
    formatShow(templateType);

    var hasChange = $('#aceList .active').attr('data-change');
    if (!hasChange || hasChange !== 'yes') {
        insertTemplate(true);
        setTimeout(function () {
            $('#aceList .active').attr('data-change', '');
        }, 50);
    }
    */
});

new ClipboardJS('.ace-editor-copy', {
    text: function (trigger) {
        var value = aceEditor[0].getValue();
        if (value) {
            return value;
        } else {
            return false;
        }
    }
});

//复制网址
new ClipboardJS('.website-copy', {
    text: function (trigger) {
        var value = 'http://www.kjson.com';
        if (value) {
            msgSuccess('网址复制成功');
            return value;
        } else {
            return false;
        }
    }
});

//复制输出
new ClipboardJS('#outputCopy', {
    text: function (trigger) {
        // var value = aceEditorOutput.getValue();
        var value = aceEditorOutput.text();
        if (value) {
            msgSuccess('复制成功');
            return value;
        } else {
            return false;
        }
    }
});

//下载输出
$('#outputDownload').click(function () {
    // var code = aceEditorOutput.getValue();
    var code = aceEditorOutput.text();
    var name = 'output.txt';
    downloadZipRunCode(name, code);
});

//输出最大化
$('#outputFullscreen').click(function () {
    var type = $(this).attr('data-full');
    $('#putOutPutBox').toggleClass('widthandmaxwidth-100');
    if (type === 'no') {
        $('.output-box').addClass('output-fullscreen');
        $('#putBoxOutput').height(windowHeight);
        $(this).attr('data-full', 'yes');
    } else {
        $('.output-box').removeClass('output-fullscreen');
        $('#putBoxOutput').height('');
        $(this).attr('data-full', 'no');
    }
    // aceEditorOutput.resize()
});

// 你需要手动初始化工具提示
$('[data-toggle="tooltip"]').tooltip();

//插入模板
$('#insertTemplate').click(function () {
    var hasChange = $('#aceList .active').attr('data-change');
    if (!hasChange || hasChange !== 'yes') {
        return;
    } else {
        alertConfirm('此操作将覆盖您修改的代码，您确定要插入模板吗？', '', '', function () {
            $('#aceList .active').attr('data-change', '');
            insertTemplate(true);
            setTimeout(function () {
                $('#aceList .active').attr('data-change', '');
            }, 50);
        });
    }
});

//上传本地代码到当前编辑器
function openFile(event) {
    var input = event.target;
    var reader = new FileReader();
    var name = input.files[0].name.split('.')[input.files[0].name.split('.').length - 1];
    var type = templates[templateType].name.split('.')[1];
    if (name !== type && name !== 'txt') {
        msgError('请上传.' + type + ' 或者.txt文件');
        return;
    }
    reader.onload = function () {
        if (reader.result) {
            //显示文件内容
            var index = $('#aceList .active').index();
            aceEditor[index].setValue('');
            aceEditor[index].insert(reader.result);
        }
    };
    reader.readAsText(input.files[0]);
}

function openFileImport(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function () {
        if (reader.result) {
            //显示文件内容
            aceEditorInput.setValue('');
            aceEditorInput.insert(reader.result);
        }
    };
    reader.readAsText(input.files[0]);
}

var Base64 = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(e) {
        var t = "";
        var n, r, i, s, o, u, a;
        var f = 0;
        e = Base64._utf8_encode(e);
        while (f < e.length) {
            n = e.charCodeAt(f++);
            r = e.charCodeAt(f++);
            i = e.charCodeAt(f++);
            s = n >> 2;
            o = (n & 3) << 4 | r >> 4;
            u = (r & 15) << 2 | i >> 6;
            a = i & 63;
            if (isNaN(r)) {
                u = a = 64
            } else if (isNaN(i)) {
                a = 64
            }
            t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
        }
        return t
    },
    decode: function(e) {

        console.log(e);

        var t = "";
        var n, r, i;
        var s, o, u, a;
        var f = 0;
        e = e.replace(/[^A-Za-z0-9+/=]/g, "");
        while (f < e.length) {
            s = this._keyStr.indexOf(e.charAt(f++));
            o = this._keyStr.indexOf(e.charAt(f++));
            u = this._keyStr.indexOf(e.charAt(f++));
            a = this._keyStr.indexOf(e.charAt(f++));
            n = s << 2 | o >> 4;
            r = (o & 15) << 4 | u >> 2;
            i = (u & 3) << 6 | a;
            t = t + String.fromCharCode(n);
            if (u != 64) {
                t = t + String.fromCharCode(r)
            }
            if (a != 64) {
                t = t + String.fromCharCode(i)
            }
        }
        t = Base64._utf8_decode(t);
        return t
    },
    _utf8_encode: function(e) {
        e = e.replace(/rn/g, "n");
        var t = "";
        for (var n = 0; n < e.length; n++) {
            var r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r)
            } else if (r > 127 && r < 2048) {
                t += String.fromCharCode(r >> 6 | 192);
                t += String.fromCharCode(r & 63 | 128)
            } else {
                t += String.fromCharCode(r >> 12 | 224);
                t += String.fromCharCode(r >> 6 & 63 | 128);
                t += String.fromCharCode(r & 63 | 128)
            }
        }
        return t
    },
    _utf8_decode: function(e) {
        var t = "";
        var n = 0;
        var r = c1 = c2 = 0;
        while (n < e.length) {
            r = e.charCodeAt(n);
            if (r < 128) {
                t += String.fromCharCode(r);
                n++
            } else if (r > 191 && r < 224) {
                c2 = e.charCodeAt(n + 1);
                t += String.fromCharCode((r & 31) << 6 | c2 & 63);
                n += 2
            } else {
                c2 = e.charCodeAt(n + 1);
                c3 = e.charCodeAt(n + 2);
                t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
                n += 3
            }
        }
        return t
    }
};


// var $iframeDoc = document.getElementById("resultPreview").contentWindow.document;

function get_result() {
    $.get("//runcode.bejson.com/try_run?action=get_result&token="+token,function (data) {
        if(typeof data.status !="undefined" && typeof data.status.description !="undefined" && data.status.description=='Accepted')
        {
            var html="";
            if (data.stderr!=null)
                html+="<div><b>标准错误：</b></div><pre>"+(Base64.decode(data.stderr)+"")+"</pre>";
            if (data.stdout!=null)
                html+="<div><b>标准输出：</b></div><pre>"+(Base64.decode(data.stdout)+"")+"</pre>";
            output_result(html);
            $('#runCode').button('reset')
        }
        else if(typeof data.status !="undefined" && typeof data.status.description !="undefined" && data.status.description=='Compilation Error')
        {
            var html="";
            if (data.compile_output!=null)
            {
                var compile_output=Base64.decode(data.compile_output);
                html+="<div><b>编译错误：</b></div><pre>"+(compile_output+"")+"</pre>";
            }
            output_result(html);
            $('#runCode').button('reset')
        }
        else if(typeof data.status !="undefined" && typeof data.status.description !="undefined" && data.status.description=='Time Limit Exceeded')
        {
            var html="";
            if (data.message!=null)
            {
                var message=Base64.decode(data.message);
                html+="<div><b>编译错误：</b></div><pre>"+(message+"")+"</pre>";
            }
            output_result(html);
            $('#runCode').button('reset')
        }
        else if(typeof data.status !="undefined" && typeof data.status.description !="undefined" && data.status.description.indexOf('Runtime Error')>-1)
        {
            var html="";
            if (data.status.description!=null)
            {
                var compile_output=(data.status.description);
                var std_output="";
                if(data.stdout)
                    std_output+=Base64.decode(data.stdout);
                if(data.stderr)
                    std_output+=Base64.decode(data.stderr);
                html+="<div><b>编译错误：</b></div><pre>"+(compile_output+"")+"</pre>";
                html+="<div><b>执行错误：</b></div><pre>"+(std_output+"")+"</pre>";
            }
            output_result(html);
            $('#runCode').button('reset')
        }

        else if(typeof data.error!="undefined")
        {
            var html="无法执行编译操作，请检查错误。";
            output_result(html);
            $('#runCode').button('reset')
        }
        else
        {
            window.setTimeout(get_result,1000)
        }
    },'json');
}

function output_result(r) {
    $('#runCode').button('reset');
    // aceEditorOutput.setValue(r);
    aceEditorOutput.html(r);
    $('.output-status').text('Accept');
}

function codeRun() {
    var index = $('#aceList .active').index();
    var codeParam = ($('#cmdParam').val());
    var codeSource = (aceEditor[index].getValue());
    var codeImport = (aceEditorInput.getValue());

    var language_id=($("#aceEditorTypeList>option:selected").attr('lid'));

    aceEditorOutput.html('正在获取运行结果...');

    $.post('//runcode.bejson.com/try_run?action=get_token',{source_code:codeSource,language_id:language_id,command_line_arguments:codeParam,stdin:codeImport},function (data) {
        if(typeof data.token=="undefined")
        {
            alertError({"con": '未知错误'})
        }
        else
        {
            token=data.token;
            get_result(token);
        }
    },'json');


    /*
    var param = {
        param: codeParam,
        source: codeSource,
        import: codeImport
    };
    $('.output-status').text('');
    $('.output-speed').text('Runing...');
    $.ajax({
        url: '',
        data: param,
        success: function () {

        }, error: function () {
            setTimeout(function () {
                $('#runCode').button('reset');
                aceEditorOutput.setValue('Hello World ' + new Date().getTime());
                $('.output-status').text('Accept');
                $('.output-speed').text('0.003s, 3668KB');
            }, 2000);
        }
    });
    */
}


//监听keycode
$(document).keydown(function (event) {
    //运行功能
    if ((event.ctrlKey && event.keyCode === 13) || event.keyCode === 120) {
        console.log(111)
        $('#runCode').trigger('click');
    }
});

//插入新的ace窗口
$('#acePlus').click(function () {
    if ($('#aceList li').length > 5) {
        msgError('只能显示6个窗口');
        return;
    }
    $('#aceList li').removeClass('active');
    $('#aceEditorContain .ace-box .ace-editor-cus').addClass('custom-displaynone');
    var index = $('#aceList li').length;
    var editorCon = insertTemplate(false);
    var li = document.createElement('li');
    li.className = 'active';
    li.innerHTML = '<span>' + editorCon.name + '</span><i class="icon icon-times"></i>';
    li.setAttribute('data-type', templateAceType);
    $('#aceList').append(li);
    // $('#aceList').append('<li class="active" data-type="'+templateAceType+'"><span>'+editorCon.name+'</span><i class="icon icon-times"></i></li>');
    var div = document.createElement('div');
    div.className = 'ace-editor-cus';
    $('#aceEditorContain .ace-box').append(div);
    //初始化ace编辑器
    aceEditor[index] = ace.edit(div);
    aceEditor[index].getSession().setMode(templateAceType);
    aceEditor[index].session.setOptions(aceSessionOptions);
    var localAceTheme2 = localStorage.getItem('aceTheme');
    aceEditor[index].setTheme(localAceTheme2 ? localAceTheme2 : 'ace/theme/github');
    aceEditor[index].setOptions(aceOptions);
    //初始化编辑器内容
    var editorHtml = editorCon.template;
    aceEditor[index].setValue('');
    aceEditor[index].focus();
    aceEditor[index].insert(editorHtml);
    aceEditor[index].getSession().on('change', function () {
        li.setAttribute('data-change', 'yes');
    });
});
//窗口切换
$('body').on('click', '#aceList li', function () {
    if ($(this).hasClass('active')) {
        return;
    }
    var type = $(this).attr('data-type');
    $('#aceEditorTypeList').val(type);
    templateAceType = type;
    templateType = type.split('/')[2];
    $('#aceEditorTypeList').trigger('chosen:updated');
    $('#aceList li').removeClass('active');
    $(this).addClass('active');
    $('#aceEditorContain .ace-box .ace-editor-cus').addClass('custom-displaynone');
    var index = $(this).index();
    $('#aceEditorContain .ace-box').find('.ace-editor-cus').eq(index).removeClass('custom-displaynone');
    aceEditor[index].focus();
    formatShow(templateType);
});
//窗口关闭
$('body').on('click', '#aceList li .icon-times', function (e) {
    e.stopPropagation();
    var index = $(this).parent().index() - 1;
    var index2 = $(this).parent().index();
    if ($(this).parent().hasClass('active')) {
        $('#aceList li').removeClass('active');
        $('#aceList').find('li').eq(index).addClass('active');
        $('#aceEditorContain .ace-box .ace-editor-cus').addClass('custom-displaynone');
        $('#aceEditorContain .ace-box').find('.ace-editor-cus').eq(index).removeClass('custom-displaynone');
        aceEditor[index].focus();
        var type = $('#aceList').find('li').eq(index).attr('data-type');
        $('#aceEditorTypeList').val(type);
        templateAceType = type;
        templateType = type.split('/')[2];
        $('#aceEditorTypeList').trigger('chosen:updated');
    }
    $(this).parent().remove();
    aceEditor[index2].destroy();
    aceEditor[index2].container.remove();
    aceEditor.splice(index2, 1);
    formatShow(templateType);
});
//收起和展开功能按钮
$('#expandFeatures').click(function(){
    $(this).parent().find('.features-import').toggle();
    $('#runCode span').toggle();
    $(this).find('.icon-align-justify').toggle();
    $(this).find('.icon-times').toggle();
})