import { NextResponse } from "next/server";

export function middleware(request) {
  const hostname = request.headers.get("host") || "localhost";
  const url = request.nextUrl.clone();
  url.searchParams.set("hostname", hostname);
  return NextResponse.rewrite(url);
}
