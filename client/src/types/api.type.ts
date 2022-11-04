export interface UserLoginRequest extends RequestInit {
    headers: {
        'Content-Type': string;
        Accept: string;
        'X-CSRFToken': string;
    }
}
export interface UserLogoutRequest extends RequestInit {
    headers: {
        'Content-Type': string;
        Accept: string;
        'X-CSRFToken': string;
    }
}

export interface ManagemResponse extends ResponseInit {
    message: string;
}