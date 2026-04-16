import { PrivateRouteGuard } from "@/modules/auth/components/PrivateRouteGuard";
import { Navbar } from "@/shared/ui/Navbar";

type IdeasLayoutProps = {
  children: React.ReactNode;
};

export default function IdeasLayout({ children }: IdeasLayoutProps) {
  return (
    <PrivateRouteGuard>
      <Navbar />
      {children}
    </PrivateRouteGuard>
  );
}
