# /// script
# dependencies =["nanodjango"]
# ///

from django.db import models
from nanodjango import Django
from django.shortcuts import render, redirect

app = Django()

class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


@app.route("/")
def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority")
        Task.objects.create(title=title, priority=priority)
        return redirect("/")
    tasks = Task.objects.order_by("completed","-priority", "-created",)
    ctx = {"tasks": tasks}
    return render(request, "index.html", ctx)

@app.route("/complete/<int:id>")
def complete(request, id):
    task = Task.objects.get(id=id)
    task.completed = True
    task.save()
    
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="localhost")


# uv run app.py