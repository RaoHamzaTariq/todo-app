import TaskForm from "@/components/tasks/TaskForm";

export default function NewTaskPage() {
  return (
    <div className="flex justify-center items-center min-h-[calc(100vh-200px)] py-12">
      <TaskForm mode="create" />
    </div>
  );
}
