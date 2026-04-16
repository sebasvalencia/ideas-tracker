"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { clearAccessToken, getTokenEmail } from "@/modules/auth/services/tokenSession";
import styles from "@/shared/ui/Navbar.module.scss";

export function Navbar() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [email] = useState<string | null>(() => getTokenEmail());
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function onClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, [open]);

  function handleLogout() {
    clearAccessToken();
    router.replace("/login");
  }

  const initials = email ? email[0].toUpperCase() : "?";

  return (
    <nav className={styles.nav}>
      <div className={styles.brand}>
        <svg
          aria-hidden="true"
          className={styles.brandIcon}
          fill="none"
          height="20"
          viewBox="0 0 24 24"
          width="20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 2a7 7 0 0 1 5.292 11.584C16.57 14.648 16 15.8 16 17v1H8v-1c0-1.2-.57-2.352-1.292-3.416A7 7 0 0 1 12 2Z"
            stroke="currentColor"
            strokeLinejoin="round"
            strokeWidth="1.5"
          />
          <path d="M9 21h6" stroke="currentColor" strokeLinecap="round" strokeWidth="1.5" />
          <path d="M10 18h4" stroke="currentColor" strokeLinecap="round" strokeWidth="1.5" />
        </svg>
        <span className={styles.brandName}>Ideas Tracker</span>
      </div>

      <div className={styles.userArea} ref={ref}>
        <button
          aria-expanded={open}
          aria-label="User menu"
          className={styles.avatarButton}
          onClick={() => setOpen((prev) => !prev)}
          type="button"
        >
          <span className={styles.avatar}>{initials}</span>
          <svg
            aria-hidden="true"
            className={`${styles.chevron} ${open ? styles.chevronOpen : ""}`}
            fill="none"
            height="12"
            viewBox="0 0 12 12"
            width="12"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2 4l4 4 4-4"
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="1.5"
            />
          </svg>
        </button>

        {open && (
          <div className={styles.dropdown} role="menu">
            {email && <p className={styles.dropdownEmail}>{email}</p>}
            <hr className={styles.divider} />
            <button
              className={styles.dropdownItem}
              onClick={handleLogout}
              role="menuitem"
              type="button"
            >
              <svg
                aria-hidden="true"
                fill="none"
                height="14"
                viewBox="0 0 24 24"
                width="14"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="1.75"
                />
              </svg>
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
