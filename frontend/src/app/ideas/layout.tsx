import { PrivateRouteGuard } from "@/modules/auth/components/PrivateRouteGuard";

type IdeasLayoutProps = {
  children: React.ReactNode;
};

export default function IdeasLayout({ children }: IdeasLayoutProps) {
  return <PrivateRouteGuard>{children}</PrivateRouteGuard>;
}
