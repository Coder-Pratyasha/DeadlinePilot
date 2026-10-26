import { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

function Layout({ children }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen overflow-x-hidden bg-transparent">
      <Sidebar
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
      />

      <main className="min-h-screen lg:pl-64">
        <div className="mx-auto w-full max-w-[1500px] px-4 py-4 sm:px-6 sm:py-5 lg:px-10">
          <Header
            mobileMenuOpen={mobileMenuOpen}
            setMobileMenuOpen={setMobileMenuOpen}
          />

          <div className="animate-page-in">{children}</div>
        </div>
      </main>
    </div>
  );
}

export default Layout;