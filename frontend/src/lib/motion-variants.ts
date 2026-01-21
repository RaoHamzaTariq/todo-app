import { Variants } from "framer-motion";

// Reusable animation variants
export const fadeIn: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: "easeOut" } },
    exit: { opacity: 0, y: -20, transition: { duration: 0.2 } }
};

export const scaleIn: Variants = {
    initial: { scale: 0.9, opacity: 0 },
    animate: { scale: 1, opacity: 1, transition: { duration: 0.3, type: "spring", stiffness: 300 } },
    exit: { scale: 0.9, opacity: 0, transition: { duration: 0.2 } }
};

export const staggerContainer: Variants = {
    animate: { transition: { staggerChildren: 0.1 } }
};

export const pulseRing: Variants = {
    animate: {
        boxShadow: [
            "0 0 0 0 rgba(59, 130, 246, 0.4)",
            "0 0 0 10px rgba(59, 130, 246, 0)"
        ],
        transition: { duration: 1.5, repeat: Infinity }
    }
};

export const messageEnter: Variants = {
    initial: { opacity: 0, y: 30, scale: 0.95 },
    animate: {
        opacity: 1,
        y: 0,
        scale: 1,
        transition: { duration: 0.4, type: "spring", stiffness: 200, damping: 20 }
    }
};

export const slideUp: Variants = {
    initial: { opacity: 0, y: 50 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.4, type: "spring" } },
    exit: { opacity: 0, y: 50, transition: { duration: 0.3 } }
};

export const dotsPulse: Variants = {
    initial: { opacity: 0.3 },
    animate: {
        opacity: [0.3, 1, 0.3],
        transition: { duration: 1.5, repeat: Infinity, ease: "easeInOut" }
    }
};