import { test, expect, afterEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import { ToolInvocationDisplay } from "../ToolInvocationDisplay";

afterEach(() => {
  cleanup();
});

test("shows 'Creating' for str_replace_editor create command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "1",
        toolName: "str_replace_editor",
        args: { command: "create", path: "app/page.tsx" },
        state: "result",
        result: "Success",
      }}
    />
  );

  expect(screen.getByText("Creating app/page.tsx")).toBeDefined();
});

test("shows 'Editing' for str_replace_editor str_replace command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "2",
        toolName: "str_replace_editor",
        args: { command: "str_replace", path: "lib/utils.ts" },
        state: "result",
        result: "Success",
      }}
    />
  );

  expect(screen.getByText("Editing lib/utils.ts")).toBeDefined();
});

test("shows 'Editing' for str_replace_editor insert command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "3",
        toolName: "str_replace_editor",
        args: { command: "insert", path: "index.ts" },
        state: "result",
        result: "Success",
      }}
    />
  );

  expect(screen.getByText("Editing index.ts")).toBeDefined();
});

test("shows 'Reading' for str_replace_editor view command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "4",
        toolName: "str_replace_editor",
        args: { command: "view", path: "README.md" },
        state: "result",
        result: "file contents",
      }}
    />
  );

  expect(screen.getByText("Reading README.md")).toBeDefined();
});

test("shows 'Deleting' for file_manager delete command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "5",
        toolName: "file_manager",
        args: { command: "delete", path: "old-file.ts" },
        state: "result",
        result: { success: true },
      }}
    />
  );

  expect(screen.getByText("Deleting old-file.ts")).toBeDefined();
});

test("shows 'Renaming' for file_manager rename command", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "6",
        toolName: "file_manager",
        args: { command: "rename", path: "old.ts", new_path: "new.ts" },
        state: "result",
        result: { success: true },
      }}
    />
  );

  expect(screen.getByText("Renaming old.ts")).toBeDefined();
});

test("falls back to raw tool name for unknown tools", () => {
  render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "7",
        toolName: "some_unknown_tool",
        args: {},
        state: "result",
        result: "done",
      }}
    />
  );

  expect(screen.getByText("some_unknown_tool")).toBeDefined();
});

test("shows spinner when state is not result", () => {
  const { container } = render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "8",
        toolName: "str_replace_editor",
        args: { command: "create", path: "app/page.tsx" },
        state: "call",
      }}
    />
  );

  expect(container.querySelector(".animate-spin")).toBeDefined();
  expect(container.querySelector(".bg-emerald-500")).toBeNull();
});

test("shows green dot when state is result", () => {
  const { container } = render(
    <ToolInvocationDisplay
      tool={{
        toolCallId: "9",
        toolName: "str_replace_editor",
        args: { command: "create", path: "app/page.tsx" },
        state: "result",
        result: "Success",
      }}
    />
  );

  expect(container.querySelector(".bg-emerald-500")).toBeDefined();
});
