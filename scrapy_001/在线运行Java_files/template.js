//初始化当前编辑器类型
var localTemplateType = localStorage.getItem('templateType');
var templateType = localTemplateType ? localTemplateType : $('#aceEditorTypeList option:selected').val().split('/')[2];
var localtemplateAceType = localStorage.getItem('templateAceType');
var templateAceType = localtemplateAceType ? localtemplateAceType : $('#aceEditorTypeList option:selected').val();
//初始化插入编辑器模板列表
var templates = {
    html: {
        template: '<!DOCTYPE html>',
        name: 'html.html'
    },
    php: {
        template: '' +
        '<?php\n' +
        'print("Hello, World\\n");\n' +
        '?>',
        name: 'main.php'
    },
    'mode-assembly_x86':{
        template: '' +
        '[section .data]         ;  // 注释\n' +
        '    strHello db "Hello,world!", 0Ah\n' +
        '    STRLEN equ $ - strHello\n' +
        '    [section .text]  ; \n' +
        '    global _start    ; \n' +
        ' \n' +
        '_start:\n' +
        '    mov edx, STRLEN\n' +
        '    mov ecx, strHello\n' +
        '    mov ebx, 1\n' +
        '    mov eax, 4    ;  sys_write\n' +
        '    int 0x80         ;  系统调用\n' +
        '    mov ebx, 0\n' +
        '    mov eax, 1    ;  sys_exit\n' +
        '    int 0x80         ;  系统调用',
        name: 'main.asm'
    }
    ,'bash': {
        template: '' +
        'echo Hello,world' +
        '',
        name: 'bash.sh'
    },
    'basic': {
        template: '' +
        'PRINT "Hello, World"' +
        '',
        name: 'basic.txt'
    },
    'c': {
        template: '' +
        '#include <stdlib.h>\n' +
        ' \n' +
        'int main()\n' +
        '{\n' +
        '    printf("Hello, World");\n' +
        '    return(0);\n' +
        '}',
        name: 'hello.c'
    },
    'csharp': {
        template: '' +
        'using System;\n' +
        'class Program\n' +
        '{\n' +
        '    public static void Main(string[] args)\n' +
        '    {\n' +
        '        Console.WriteLine("Hello, World");\n' +
        '    }\n' +
        '}',
        name: 'hello.cs'
    },
    'c_cpp': {
        template: '' +
        '#include <iostream>\n' +
        ' \n' +
        'int main()\n' +
        '{\n' +
        '    std::cout << "Hello World";\n' +
        '    return 0;\n' +
        '}',
        name: 'hello.cpp'
    },
    'clojure': {
        template: '' +
        '(println "hello world")',
        name: 'clojure'
    },
    'cobol': {
        template: '' +
        'IDENTIFICATION DIVISION.\n' +
        'PROGRAM-ID. hello.\n' +
        'PROCEDURE DIVISION.\n' +
        'DISPLAY "Hello, world!".\n' +
        'STOP RUN.',
        name: 'cobol'
    },
    'commonlisp': {
        template: '' +
        '(defun hello-world()\n' +
        '      (format t "Hello,World!"))\n' +
        '\n' +
        '(hello-world)',
        name: 'common_lisp'
    },
    'd': {
        template: '' +
        'import std.stdio;\n' +
        '\n' +
        'void main()\n' +
        '{\n' +
        '    writeln("Hello World");\n' +
        '}',
        name: 'helloword.d'
    },
    'elixir': {
        template: 'IO.puts "hello word"',
        name: 'elixir'
    },
    'erlang': {
        template: '' +
        'main(_) ->\n' +
        '\tio:fwrite("Hello, World\\n").\n',
        name: 'main.erlang'
    },
    'executable': {
        template: '',
        name: 'main.executable'
    },
    'fsharp': {
        template: 'printfn "hello world"',
        name: 'main.f'
    },
    'fortran': {
        template: '' +
        'program main\n' +
        '\tprint *, "Hello, World"\n' +
        'end\n',
        name: ''
    },
    'golang': {
        template: '' +
        'package main\n' +
        '\n' +
        'import "fmt"\n' +
        '\n' +
        'func main() {\n' +
        '    fmt.Println("Hello world!")\n' +
        '}',
        name: 'main.go'
    },
    'groovy': {
        template: '',
        name: 'main.groovy'
    },
    'haskell': {
        template: 'main = putStrLn "Hello, World"',
        name: 'main.haskell'
    },
    'java': {
        template: '' +
        'public class Main {\n' +
        '\tpublic static void main(String[] args) {\n' +
        '\t\tSystem.out.println("Hello, World");\n' +
        '\t}\n' +
        '}\n',
        name: 'main.java'
    },
    'javascript': {
        template: '' +
        'console.log("Hello, World");',
        name: 'main.js'
    },
    'kotlin': {
        template: '' +
        'fun main() {\n' +
        '\tprintln("Hello, World")\n' +
        '}\n',
        name: 'main.kt'
    },
    'lua': {
        template: '' +
        'print("Hello, World")',
        name: 'main.lua'
    },
    'object_c': {
        template: '' +
        '#import <Foundation/Foundation.h>\n' +
        ' \n' +
        'int main(int argc, const char * argv[]) {\n' +
        '    @autoreleasepool {\n' +
        '        NSLog(@"Hello, World!");\n' +
        '    }\n' +
        '     return 0;\n' +
        '}',
        name: 'main.c'
    },
    'ocaml': {
        template: 'print_endline "Hello, World"',
        name: 'main.oc'
    },
    'octave': {
        template: 'printf("Hello, World\\n");',
        name: 'main.octave'
    },
    'pascal': {
        template: '' +
        'program Hello;\n' +
        'begin\n' +
        '\twriteln (\'Hello, World\')\n' +
        'end.\n',
        name: 'main.pas'
    },
    'perl': {
        template: '' +
        '#!/usr/bin/perl \n' +
        ' \n' +
        'print "Hello, World!\\n";',
        name: 'main.perl'
    },
    'plain': {
        template: 'Hello, World',
        name: 'main.plain'
    },
    'prolog': {
        template: '' +
        ':- initialization(main).\n' +
        'main :- write(\'Hello, World\\n\').\n',
        name: 'main.prolog'
    },
    'python': {
        template: '' +
        'import sys\n' +
        'import os\n' +
        'print "Hello,World"',
        name: 'main.py'
    },
    'python3': {
        template: '' +
        'import sys\n' +
        'import os\n' +
        'print("Hello,World")',
        name: 'main.py3'
    },
    'r': {
        template: '' +
        'cat("Hello, World\\n")',
        name: 'main.r'
    },
    'ruby': {
        template: '' +
        'puts "Hello, World"',
        name: 'main.ruby'
    },
    'rust': {
        template: '' +
        'fn main() {\n' +
        '\tprintln!("Hello, World");\n' +
        '}\n',
        name: 'main.ru'
    },
    'scala': {
        template: '' +
        'object Main {\n' +
        '\tdef main(args: Array[String]) = {\n' +
        '\t\tprintln("Hello, World")\n' +
        '\t}\n' +
        '}\n',
        name: 'main.sc'
    },
    'sql': {
        template: '' +
        'CREATE TABLE Person (\n' +
        '\tPersonID int,\n' +
        '\tLastName varchar(255),\n' +
        '\tFirstName varchar(255),\n' +
        '\tAddress varchar(255),\n' +
        '\tCity varchar(255)\n' +
        ');\n' +
        '\n' +
        'INSERT INTO Person VALUES (1, \'Tom\', \'Erichsen\', \'Skagen 210, Stavanger 4006\', \'Norway\');\n' +
        '\n' +
        'SELECT * FROM Person;\n',
        name: 'main.sql'
    },
    'swift': {
        template: '' +
        'print("Hello, World")',
        name: 'main.sw'
    },
    'typescript': {
        template: '' +
        'console.log("Hello, World");',
        name: 'main.ts'
    },
    'vbscript': {
        template: '' +
        'Public Module Program\n' +
        '\t Public Sub Main()\n' +
        '\t\tConsole.WriteLine("Hello, World")\n' +
        '\t End Sub\n' +
        'End Module\n',
        name: 'main.vs'
    },
};

//获取模板内容或则插入模板
function insertTemplate(editor) {
    var editorCon = templates[templateType];
    if (!templates[templateType]) {
        editorCon = {
            template: 'other',
            name: 'other.other'
        };
    }
    if (editor) {
        var index = $('#aceList .active').index();
        var hasChange = $('#aceList .active').attr('data-change');
        if (!hasChange || hasChange !== 'yes') {
            aceEditor[index].setValue('');
            aceEditor[index].insert(editorCon.template);
        }
        $('#aceList .active span').text(editorCon.name);
        $('#aceList .active').attr('data-type', templateAceType);
    } else {
        return editorCon;
    }
}

//利用localstorage获取上次设置，初始化ace编辑器
var aceEditor = [];
aceEditor[0] = ace.edit('aceEditor');
aceEditor[0].getSession().setMode(templateAceType);
var localAceTheme = localStorage.getItem('aceTheme');
aceEditor[0].setTheme(localAceTheme ? localAceTheme : 'ace/theme/github');

var aceTabSize = localStorage.getItem('aceTabSize');
var aceFoldStyle = localStorage.getItem('aceFoldStyle');
var aceSessionOptions = {
    useWrapMode: localStorage.getItem('useWrapMode') === '0' ? false : true,
    useSoftTabs: localStorage.getItem('useSoftTabs') === '0' ? false : true,
    navigateWithinSoftTabs: localStorage.getItem('navigateWithinSoftTabs') === '0' ? false : true,
    tabSize: aceTabSize ? aceTabSize : 4,
    foldStyle: aceFoldStyle ? aceFoldStyle : 'manual',
};
aceEditor[0].session.setOptions(aceSessionOptions);

var cursorStyle = localStorage.getItem('aceCursorStyle');
var printMarginColumn = localStorage.getItem('printMarginColumn');
var aceOptions = {
    enableBasicAutocompletion: localStorage.getItem('enableBasicAutocompletion') === '0' ? false : true,
    enableSnippets: localStorage.getItem('enableBasicAutocompletion') === '0' ? false : true,
    enableLiveAutocompletion: localStorage.getItem('enableBasicAutocompletion') === '0' ? false : true,
    fontSize: localStorage.getItem('aceFontSize') ? parseInt(localStorage.getItem('aceFontSize')) : 14,
    showGutter: localStorage.getItem('showGutter') === '0' ? false : true,
    cursorStyle: cursorStyle ? cursorStyle : 'ace',
    highlightActiveLine: localStorage.getItem('highlightActiveLine') === '1' ? true : false,
    highlightSelectedWord: localStorage.getItem('highlightSelectedWord') === '0' ? false : true,
    showInvisibles: localStorage.getItem('showInvisibles') === '1' ? true : false,
    hScrollBarAlwaysVisible: localStorage.getItem('hScrollBarAlwaysVisible') === '1' ? true : false,
    vScrollBarAlwaysVisible: localStorage.getItem('vScrollBarAlwaysVisible') === '1' ? true : false,
    showPrintMargin: localStorage.getItem('showPrintMargin') === '1' ? true : false,
    readOnly: localStorage.getItem('aceReadOnly') === '1' ? true : false,
    printMarginColumn: printMarginColumn ? parseInt(printMarginColumn) : 80
};


console.log(aceOptions);
console.log(aceSessionOptions);
console.log(templateAceType);
console.log(localAceTheme);


aceEditor[0].setOptions(aceOptions);
//初始化编辑器内容
aceEditor[0].setValue('');
aceEditor[0].focus();
var initTemplateCon = insertTemplate(false);
aceEditor[0].insert(initTemplateCon.template);
$('#aceList li span').eq(0).text(initTemplateCon.name);//初始化标签内容
$('#aceList li').eq(0).attr('data-type', templateAceType);//初始化标签data-type
//当主编辑器内容改变时，给标签加上data-change属性，用来监视插入固定模板时的状态
aceEditor[0].getSession().on('change', function () {
    $('#aceList').find('li').eq(0).attr('data-change', 'yes');
});

//初始化输入和输出编辑器
var aceEditorInput = ace.edit('aceEditorInput');
// var aceEditorOutput = ace.edit('aceEditorOutput');
var aceEditorOutput = $('#aceEditorOutput');

aceEditorInput.setOptions({
    highlightActiveLine: false,
    highlightSelectedWord: false,
    showPrintMargin: false,
    showGutter: false
});
// aceEditorOutput.setOptions({
//     highlightActiveLine: false,
//     highlightSelectedWord: false,
//     showPrintMargin: false,
//     readOnly: true,
//     showGutter: false
// });


//获取屏幕高度，设置主编辑器高度
var windowHeight = $(window).innerHeight();
// $('#aceEditorContain').height(windowHeight / 2);

//初始化多标签或者单标签
var isMutipleTabs = localStorage.getItem('mutipleTabs');
if (isMutipleTabs === '0') {
    $('#aceList li').hide();
    $('#acePlus').hide();
} else {
    $('#aceList li').show();
    $('#acePlus').show();
}

//初始化设置弹窗的值
//左侧行号
$('#lineNumber').prop('checked', aceOptions.showGutter);
//自动补全
$('#autoComplete').prop('checked', aceOptions.enableBasicAutocompletion);
//自动换行
$('#lineWarp').prop('checked', aceSessionOptions.useWrapMode);
//多个标签
$('#mutipleTabs').prop('checked', isMutipleTabs !== '0');
//软标签
$('#softTabs').prop('checked', aceSessionOptions.useSoftTabs);
//tabsize
$('#softTabsInput').val(aceSessionOptions.tabSize);

//主题
if (localAceTheme) {
    $('#themes').val(localAceTheme);
    $('#themes option').each(function (index, item) {
        $(item).attr('selected', false);
        if ($(item).attr('value') === localAceTheme.split('/')[2]) {
            $(item).attr('selected', true);
        }
    });
} else {

}
//字号
$('#aceFontSize').val(aceOptions.fontSize);

//光标样式
if (cursorStyle) {
    $('#cursorStyle').val(cursorStyle);
    $('#cursorStyle option').each(function (index, item) {
        $(item).attr('selected', false);
        if ($(item).attr('value') === cursorStyle) {
            $(item).attr('selected', true);
        }
    });
} else {

}

//折叠样式
if (aceFoldStyle) {
    $('#foldStyle').val(aceFoldStyle);
    $('#foldStyle option').each(function (index, item) {
        $(item).attr('selected', false);
        if ($(item).attr('value') === aceFoldStyle) {
            $(item).attr('selected', true);
        }
    });
} else {

}

//高亮当前行
$('#highlightActiveLine').prop('checked', aceOptions.highlightActiveLine);
//显示不可见字符
$('#showInvisibles').prop('checked', aceOptions.showInvisibles);
//显示纵向滚动条
$('#vScrollBarAlwaysVisible').prop('checked', aceOptions.vScrollBarAlwaysVisible);
//显示横向滚动条
$('#hScrollBarAlwaysVisible').prop('checked', aceOptions.hScrollBarAlwaysVisible);
//显示打印边距
$('#showPrintMargin').prop('checked', aceOptions.showPrintMargin);
//设置页边距
$('#printMarginColumn').val(aceOptions.printMarginColumn);
//选中文本
$('#highlightSelectedWord').prop('checked', aceOptions.highlightSelectedWord);
//是否只读
$('#readOnly').prop('checked', aceOptions.readOnly);
//实时补全
$('#enableLiveAutocompletion').prop('checked', aceOptions.enableLiveAutocompletion);