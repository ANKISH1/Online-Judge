from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import CodeSubmissionForm
from pathlib import Path
from django.conf import settings
import uuid
import subprocess
from .models import Problem, TestCase, CodeSubmission
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages







# Create your views here.
@login_required
def question_list(request):
    all_questions = Problem.objects.all()
    context = {
        'all_questions':all_questions
    }
    template = loader.get_template('all_questions.html')
    return HttpResponse(template.render(context,request))

def leaderboard(request):
    leaderboard_data = (
        CodeSubmission.objects.filter(status='Passed')
        .values('user__username')
        .annotate(total_problems_solved=Count('problem', distinct=True))
        .order_by('-total_problems_solved')
    )

    context = {
        'leaderboard_data': leaderboard_data,
    }

    return render(request, 'leaderboard.html', context)

# def question_detail(request, problem_id):
#     question= get_object_or_404(Problem, id = problem_id)
#     context = {
#         'question':question
#     }
#     template = loader.get_template('index.html')
#     return HttpResponse(template.render(context, request))



def submit(request, problem_id):
    question = get_object_or_404(Problem, id=problem_id)
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            print(submission.language)
            print(submission.code)
            if "run_code" in request.POST:
                output = run_code(submission.language, submission.code, submission.input_data)
                print(f"Generated Output: {output}")
                return JsonResponse({'output': output})

            elif "submit_code" in request.POST:
                submission.save()

                test_cases = TestCase.objects.filter(problem=question)
                all_testcase_passed = True
                failed_cases = []

                for test_case in test_cases:
                    output = run_code(submission.language, submission.code, test_case.input_data)
                    print(f"Generated Output: {output}")

                    if output.strip() != test_case.expected_output.strip():
                        all_testcase_passed = False
                        failed_cases.append({
                            "input":test_case.input_data,
                            "expected_output":test_case.expected_output,
                            "actual_output": output
                        })
                    submission.output_data = output
                if all_testcase_passed:
                    submission.status = "Passed"
                    submission.result = "All test cases passed"
                else:
                    submission.status = "Failed"
                    submission.result = f"{len(failed_cases)} test cases failed."

            submission.save()
            return JsonResponse({
                'status':submission.status,
                'result':submission.result,
                'output': submission.output_data,
                'failed_cases': failed_cases
            })
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    else:
        form = CodeSubmissionForm()
        context = {
            'form':form,
            'question':question
        }

        return render(request, "index.html", context)

def run_code(language, code, input_data):
    input_data= input_data.replace('\r\n','\n')
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    print(f"Code file path: {code_file_path}")
    print(f"Input file path: {input_file_path}")
    print(f"Output file path: {output_file_path}")

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass

    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["g++", str(code_file_path), "-o", str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
    elif language == "py":
        with open(input_file_path, "r") as input_file:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )

    with open(output_file_path,"r") as output_file:
        output_data = output_file.read()

    return output_data


def post_logout(request):
    logout(request)
    messages.info(request, 'logout successful')
    return redirect('/auth/login/')

