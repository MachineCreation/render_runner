
# -------------------------------------------------------------------------------
# Render_runner Main UI
# Joseph Egan
# 2026-03-25
# Sources: 
# -------------------------------------------------------------------------------
# Description: Class that holds the main UI for creating, viewing and aborting
# render jobs

# Local imports
from app.Logic.processing import validations, helpers
from app.Logic.Jobs.Job import Job
from app.Logic.workflow.workflows import get_templates
from app.Data.Database import Database

# python imports
from datetime import timedelta


class UI:

    __job_queue: list[Job] = []
    __db = Database()

    
    def start(self):
        while True:
            main_options = {
                1: ['Create New Job', 'create_job'],
                2: ['View jobs', 'view_jobs'],
                3: ['Abort Queued Job', 'abort_job'],
                4: ['Quit', 'quit_ui']
            }

            print("Choose option below")

            for index, option in main_options.items():
                print(f"{index}. {option[0]}")

            choice = validations.input_int(prompt='', gt=0, le=len(main_options))

            method_name = main_options.get(choice)[1]
            if method_name == 'quit_ui':
                self.quit_ui()
                break
            # print(method_name)

            method = self.__getattribute__(method_name)
            method()

# -----------------------------------menu functions---------------------------
    # -------------------
    def create_job(self):
        '''
        menu function for creating new jobs
        '''
        job_vars = []
        # input job name
        job_name = validations.input_string(
            'Enter Job name\n',
            'Name can not be blank.',
            helpers.non_empty
            )
        job_vars.append(job_name)

        # input generation prompt
        prompt = self.prompt_input()
        job_vars.append(prompt)

        # choose workflow template
        template_names, base_path = get_templates()
        template_name = validations.select_item(template_names)
        template = base_path / template_name
        # print(template)
        job_vars.append(template)

        # get generation length if generation is animated video
        is_animation = validations.input_y_or_n(
            'Is this generation an animation(video)?'
            '\n Yes/y'
            '\n No/n'
            )
        length = None if not is_animation else self.get_animation_length()
        if length:
            job_vars.append(length)
        
        # create job object
        job = Job(*job_vars)

        # verify user wants to save job
        
        print('Would you like to save this job?')
        job.print_job()
        save = validations.input_y_or_n()
        if save:
            self.__job_queue.append(job)
            job.save_job(self.__db)


    # --------------------
    def quit_ui(self):
        self.__db.close_connection()
        self.__db.delete_db_object()
        del self

# --------------------------------- helpers ---------------------------------
    @staticmethod
    def prompt_input() -> str:
        while True:
            try:
                #get prompt
                prompt = validations.input_string(
                    "Enter your generation prompt here:\n",
                    "Prompt can not be blank",
                    helpers.non_empty
                )
                # sanitize and normalize the prompt for json
                clean_prompt = validations.python_safe_prompt(prompt)

                return clean_prompt
            
            except TypeError:
                continue
            except ValueError:
                continue


    #----------------------
    @staticmethod
    def get_animation_length() -> timedelta:
        print('Length of animation is measured in minutes and seconds')
        
        minutes = validations.input_int(
            gt=0,
            lt=10,
            prompt='Enter Minutes\n'
            )
        
        seconds = validations.input_int(
            ge=0,
            le=59,
            prompt='Enter Seconds\n'
        )

        return timedelta(minutes=minutes, seconds=seconds)
        