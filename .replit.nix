{ pkgs }: {
  deps = [
    pkgs.psmisc
    pkgs.glibcLocales
    pkgs.cacert
    pkgs.libxcrypt

    pkgs.gcc            # Añadimos gcc para compilar dependencias nativas
    pkgs.libstdcxx6     # 🔥 CORRIGE el error de libstdc++.so.6 para faiss y torch

    pkgs.python311
    pkgs.python311Packages.pillow
    pkgs.python311Packages.streamlit
    pkgs.python311Packages.numpy
    pkgs.python311Packages.tqdm
    pkgs.python311Packages.python_dotenv
    pkgs.python311Packages.gspread
    pkgs.python311Packages.oauth2client

    pkgs.python311Packages.pandas
    pkgs.python311Packages.requests
    pkgs.python311Packages.google_auth
    pkgs.python311Packages.google_auth_oauthlib
    pkgs.python311Packages.pydantic
    pkgs.python311Packages.pydantic_core
    pkgs.python311Packages.flask
    pkgs.python311Packages.fpdf
    pkgs.python311Packages.pypdf2
    pkgs.python311Packages.python_docx

    # Si quieres manejar modelos, transformers y torch, sería ideal instalar:
    pkgs.python311Packages.transformers
    pkgs.python311Packages.torch
  ];
}
