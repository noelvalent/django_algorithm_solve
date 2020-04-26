"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import View
from app.forms import CodeRunnerForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

class CodeRunnerView(View):
    form_class = CodeRunnerForm
    context = {
        'title': 'Code Runner',
        'message': 'Welcome, GCC TEST BAD~~~!!!!',
        'year':datetime.now().year,
    }
    template_name = 'app/coderunner.html'

    def _context_updater(self, form, msg=None, output=None):
        self.context.update({'form': form, 'output': output})
        if bool(msg):
            self.context['message'] = msg


    def _gcc_run(self, lang, code):
        from subprocess import Popen, PIPE
        is_c = False
        if lang == 'c':
            compiler = 'gcc'
            is_c = True
        elif lang == 'cpp':
            compiler = 'g++'
        else:
            raise ValueError()

        newline_splited_code_list = code.split('\n')
        src_file = 'code.{}'.format('c' if is_c else 'cpp')
        exe_file = 'run'
        with open('./{}'.format(src_file), 'wt') as src:
            for line in code:
                src.write(line)

        compile_cmd = [compiler, src_file, '-o', exe_file]
        compile_proc = Popen(compile_cmd)
        compile_proc.wait()

        run_code_cmd = ['./{}'.format(exe_file)]
        output_bstr = Popen(run_code_cmd, stdout=PIPE).communicate()[0]
        output = str(output_bstr).split('\n')

        return output

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self._context_updater(form)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                lang = form.cleaned_data['lang']
                code = form.cleaned_data['code']
                ouput_result = self._gcc_run(lang, code)

            except ValueError:
                output_result = ['뭔가 이상한데요..?'] + [x for x in form.cleaned_data.items()]

            self._context_updater(form, 'Success', output_result)
            return render(request, self.template_name, self.context)
        
        self._context_updater(form, 'Fail')
        return render(request, self.template_name, self.context)
