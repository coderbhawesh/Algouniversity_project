from pathlib import Path
from django.shortcuts import render
from compiler.forms import SubmissionForm, CodeSubmit
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
from home.models import problem, TestCase, Solution
import uuid
import subprocess
from django.contrib.auth.decorators import login_required
import os
import filecmp
# Create your views here.


def submit(request):

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            print(submission.input)

            output_data = run_code(submission.language,
                                   submission.code, submission.input)
            submission.output = output_data
            context = {
                'submission': submission
            }
            submission.save()
            template = loader.get_template('result.html')

            return HttpResponse(template.render(context, request))

            # return HttpResponse("Hello world")

            # return render(request, "result.html", context)
    else:

        form = SubmissionForm()
        context = {
            'form': form,
        }
        template = loader.get_template('index1.html')

        # return HttpResponse(template.render(context, request))
        # return HttpResponse("Hello world1")
        return render(request, "index1.html", {"form": form})


def run_code(language, code, input_data):

    project_path = Path(settings.BASE_DIR)
    directories = ['codes', 'inputs', 'outputs']

    for directory in directories:
        dir_path = project_path/directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path/'codes'
    input_dir = project_path/'inputs'
    output_dir = project_path/'outputs'

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir/code_file_name
    input_file_path = input_dir/input_file_name
    output_file_path = output_dir/output_file_name

    # prob = problem.objects.filter()

    with open(code_file_path, 'w') as code_file:
        code_file.write(code)

    with open(input_file_path, 'w') as input_file:
        input_file.write(input_data)

    with open(output_file_path, 'w') as output_file:
        pass

    if language == "cpp" or language == "c":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ['clang++', str(code_file_path), '-o', str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, 'r') as input_file:
                with open(output_file_path, 'w') as output_file:
                    subprocess.run([str(executable_path)],
                                   stdin=input_file, stdout=output_file)
        else:
            with open(output_file_path, 'w') as output_file:
                output_file.write("Compilation error")
    elif language == "py":
        with open(input_file_path, "r") as input_file:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )

    with open(output_file_path, 'r') as output_file:
        output_data = output_file.read()

    return output_data


def post12(request):

    if request.method == "POST":
        lang = request.POST.get("language")
        problem_code = request.POST.get("problemId")
        code = request.POST.get("code")

        if lang not in ["c", "cpp", "py"]:
            return HttpResponse(
                {"error": "Invalid language"}
            )

        folder_name = "InputCodes"

        os.makedirs(folder_name, exist_ok=True)
        os.makedirs("GeneratedOutput", exist_ok=True)

        curr_dir = os.getcwd()
        folder_path = os.path.join(curr_dir, folder_name)
        uniquename = uuid.uuid4().hex
        unique_filename = f"{uniquename}.{lang}"
        file_path = os.path.join(folder_path, unique_filename)

        with open(file_path, "w") as f:
            f.write(code)

        os.chdir(folder_path)

        prob = problem.objects.filter(id=problem_code).first()
        test_case = TestCase.objects.filter(problem=prob).first()
        input_test_case = test_case.input
        output_path = test_case.output
        # print(input_path)

        unique = str(uuid.uuid4())
        # code_file_name = f"{unique}.{lang}"
        input_file_name = f"{unique}.txt"
        # output_file_name = f"{unique}.txt"

        input_file_path = folder_path+"/"+input_file_name
        # output_file_path = folder_path/output_file_name

        with open(f"{input_file_path}", "w") as input_file:
            input_file.write(input_test_case)

        if lang == "c":
            # On Mac, use clang instead of gcc for compiling C code
            result = subprocess.run(
                ["clang", f"{unique_filename}", "-o", uniquename]
            )
            if result.returncode == 0:
                os.chdir(curr_dir)
                print(os.getcwd())
                # On Mac, execute the compiled executable with input redirection and output file
                with open(f"{input_file_path}", "r") as input_file:
                    with open(
                        f"./GeneratedOutput/{uniquename}.txt", "w"
                    ) as output_file:
                        output = subprocess.run(
                            [f"./InputCodes/{uniquename}"],
                            stdin=input_file,
                            stdout=output_file,
                        )

        elif lang == "cpp":
            result = subprocess.run(
                ["clang++", f"{unique_filename}", "-o", uniquename]
            )
            if result.returncode == 0:
                os.chdir(curr_dir)
                print(os.getcwd())
                # Create GeneratedOutput directory if it doesn't exist
                generated_output_dir = "./GeneratedOutput"
                os.makedirs(generated_output_dir, exist_ok=True)
                # On Mac, execute the compiled executable with input redirection and output file
                with open(f"{input_file_path}", "r") as input_file:
                    output_file_path = f"./GeneratedOutput/{uniquename}.txt"
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [f"./InputCodes/{uniquename}"],
                            stdin=input_file,
                            stdout=output_file,
                        )

        elif lang == "py":
            os.chdir(curr_dir)
            print(os.getcwd())
            # On Mac, execute the Python script with input redirection and output file
            with open(f"{input_file_path}", "r") as input_file:
                output_file_path = f"./GeneratedOutput/{uniquename}.txt"
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        ["python3", f"InputCodes/{uniquename}.py"],
                        stdin=input_file,
                        stdout=output_file,
                    )

        with open(f"GeneratedOutput/{uniquename}.txt", "r") as gen_file:
            generated_output = gen_file.read()
        with open(f"{output_path}", "r") as ref_file:
            reference_output = ref_file.read()
            # Compare the contents of the files
        verdict = "Accepted" if generated_output.strip(
        ) == reference_output.strip() else "Wrong Answer"

        # Create a Solution instance and save it to the database
        solution = Solution.objects.create(
            problem=problem,
            verdict=verdict
        )

        context = {
            'solution': solution
        }
        solution.save()
        template = loader.get_template('index3.html')
        # return HttpResponse(
        # {"output": output_data, "result": verdict}
        # )

        return HttpResponse(template.render(context, request))

    else:
        form = CodeSubmit()
        context = {
            'form': form,
        }
        template = loader.get_template('index2.html')

        # return HttpResponse(template.render(context, request))
        # return HttpResponse("Hello world1")
        return render(request, "index2.html", {"form": form})


def post(request):

    if request.method == "POST":
        language = request.POST.get("language")
        problem_code = request.POST.get("problemId")
        code = request.POST.get("code")

        if language not in ["c", "cpp", "py"]:
            return HttpResponse(
                {"error": "Invalid language"}
            )
        project_path = Path(settings.BASE_DIR)
        directories = ['codes', 'inputs', 'outputs', 'reference']

        for directory in directories:
            dir_path = project_path/directory
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)

        codes_dir = project_path/'codes'
        input_dir = project_path/'inputs'
        output_dir = project_path/'outputs'
        reference_dir = project_path/'reference'

        prob = problem.objects.filter(id=problem_code).first()
        test_case = TestCase.objects.filter(problem=prob).first()
        input_test_case = test_case.input
        output_result = test_case.output

        unique = str(uuid.uuid4())
        code_file_name = f"{unique}.{language}"
        input_file_name = f"{unique}.txt"
        output_file_name = f"{unique}.txt"
        reference_file_name = f"{unique}.txt"

        code_file_path = codes_dir/code_file_name
        input_file_path = input_dir/input_file_name
        output_file_path = output_dir/output_file_name
        reference_file_path = reference_dir/reference_file_name

        # problem = Problem.objects.filter(code=problem_code).first()

        # prob = problem.objects.filter()

        with open(code_file_path, 'w') as code_file:
            code_file.write(code)

        with open(input_file_path, 'w') as input_file:
            input_file.write(input_test_case)

        with open(output_file_path, 'w') as output_file:
            pass

        with open(reference_file_path, 'w') as reference_file:
            reference_file.write(output_result)

        if language == "cpp" or language == "c":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ['clang++', str(code_file_path), '-o', str(executable_path)]
            )
            if compile_result.returncode == 0:
                with open(input_file_path, 'r') as input_file:
                    with open(output_file_path, 'w') as output_file:
                        subprocess.run([str(executable_path)],
                                       stdin=input_file, stdout=output_file)
            else:
                with open(output_file_path, 'w') as output_file:
                    output_file.write("Compilation error")
        elif language == "py":
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        ["python3", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )

        with open(output_file_path, 'r') as output_file:
            output_data = output_file.read()

        
            
        verdict = "Accepted" if output_data.strip(
        ) == output_result.strip() else "Wrong Answer"
        
        if output_data == "Compilation error":
            verdict = "Compilation error"

        # Create a Solution instance and save it to the database
        solution = Solution.objects.create(
            problem=prob,
            verdict=verdict
        )

        context = {
            'solution': solution
        }
        solution.save()
        template = loader.get_template('index3.html')

        return HttpResponse(template.render(context, request))

    else:
        form = CodeSubmit()
        context = {
            'form': form,
        }
        template = loader.get_template('index2.html')

        # return HttpResponse(template.render(context, request))
        # return HttpResponse("Hello world1")
        return render(request, "index2.html", {"form": form})
