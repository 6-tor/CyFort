import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service'; // Certifique-se de que o caminho está correto

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    if (this.authService.isAuthenticated()) { // Verifica se o usuário está autenticado
      return true; // Permite o acesso se autenticado
    } else {
      this.router.navigate(['/login']); // Redireciona para a página de login
      return false; // Bloqueia o acesso se não autenticado
    }
  }
}