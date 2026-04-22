import type { Metadata } from "next";
import { Playfair_Display, DM_Sans } from "next/font/google";
import "./globals.css";

const playfair = Playfair_Display({
  variable: "--font-display",
  subsets: ["latin"],
  display: "swap",
});

const dmSans = DM_Sans({
  variable: "--font-body",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Aahan Desai — Product Manager & Computer Science at Northeastern",
  description:
    "Aahan Desai is a product manager and CS student at Northeastern University. PM co-op experience, ML projects, wildlife photography, and conservation advocacy.",
  openGraph: {
    title: "Aahan Desai — Product Manager & Computer Science at Northeastern",
    description:
      "Aahan Desai is a product manager and CS student at Northeastern University. PM co-op experience, ML projects, wildlife photography, and conservation advocacy.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Aahan Desai — Product Manager & Computer Science at Northeastern",
    description:
      "Aahan Desai is a product manager and CS student at Northeastern University. PM co-op experience, ML projects, wildlife photography, and conservation advocacy.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${playfair.variable} ${dmSans.variable}`}>
      <body>{children}</body>
    </html>
  );
}
