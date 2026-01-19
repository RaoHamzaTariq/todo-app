import { motion } from "framer-motion";

interface AnimatedWrapperProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right';
}

export default function AnimatedWrapper({
  children,
  delay = 0,
  duration = 0.5,
  direction = 'up'
}: AnimatedWrapperProps) {
  const getInitialPosition = () => {
    switch(direction) {
      case 'up': return { y: 20, opacity: 0 };
      case 'down': return { y: -20, opacity: 0 };
      case 'left': return { x: -20, opacity: 0 };
      case 'right': return { x: 20, opacity: 0 };
      default: return { y: 20, opacity: 0 };
    }
  };

  return (
    <motion.div
      initial={getInitialPosition()}
      animate={{ y: 0, x: 0, opacity: 1 }}
      transition={{
        duration,
        delay,
        ease: "easeOut"
      }}
    >
      {children}
    </motion.div>
  );
}