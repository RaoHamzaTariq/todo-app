import AuthForm from "@/components/AuthForm";

export default function SignInPage() {
  return (
    <div className="flex justify-center items-center py-12">
      <AuthForm type="sign-in" />
    </div>
  );
}
