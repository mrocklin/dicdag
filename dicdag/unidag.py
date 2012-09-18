# This format is used by the Tompkins scheduler
# of the form {1: (2, 3), ...} if job 1 precedes 2 and 3
# of the form {2: (), ...} if 2 is an output
# This file converts from this format to tuple-dag format

from util import reverse_dict, merge

def dag_to_backward_unidag(dag):
    def job(outvar):
        return (dag[outvar]['args'], dag[outvar]['fn'], outvar)
    return {job(outvar): tuple(job(arg) for arg in dag[outvar]['args']
                                        if  arg in dag)
            for outvar in dag}

def dag_to_unidag(dag):
    back_unidag = dag_to_backward_unidag(dag)
    reverse_unidag = reverse_dict(back_unidag)
    output_jobs = {job: () for job in back_unidag if job not in reverse_unidag}
    return merge(reverse_unidag, output_jobs)

def backward_unidag_to_dag(unidag):
    return {outvar: {'fn': fn, 'args': args} for (args, fn, outvar) in unidag}

def unidag_to_dag(unidag):
    back_unidag = reverse_dict(unidag)
    input_jobs = {job: () for job in unidag if not job in back_unidag}
    dag = backward_unidag_to_dag(merge(back_unidag, input_jobs))
    return dag
