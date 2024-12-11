// src/app/backstage/components/TextEditor.js
import React from "react";
import { Editor } from "@tinymce/tinymce-react";

const TextEditor = ({ value, onChange }) => {
    const handleEditorChange = (content) => {
        onChange(content); // 將內容同步回父元件
    };

    return (
        <div className="backstage">
            <Editor
                apiKey="ll2e3peadtuuuisl6hvyecss28hks1bwqkj73yibiiuqpj2m" // 替換為你的 TinyMCE API Key
                value={value}
                init={{
                    height: 400,
                    menubar: true,
                    plugins: [

                    ],
                    toolbar:
                        "undo redo | formatselect | bold italic underline | \
                        alignleft aligncenter alignright alignjustify | \
                        bullist numlist outdent indent | removeformat | help",
                    block_formats: "Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Preformatted=pre",

                }}
                onEditorChange={handleEditorChange}
            />
        </div>
    );
};

export default TextEditor;
